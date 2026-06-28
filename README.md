<div align="center">

# edocAI

**Enterprise Asynchronous Document Intelligence**

*Transform unstructured invoices and receipts into structured JSON — at scale, without timeouts.*

[![Next.js](https://img.shields.io/badge/Next.js-16-black?logo=next.js&logoColor=white)](https://nextjs.org/)
[![React](https://img.shields.io/badge/React-19-61DAFB?logo=react&logoColor=black)](https://react.dev/)
[![TypeScript](https://img.shields.io/badge/TypeScript-5-3178C6?logo=typescript&logoColor=white)](https://www.typescriptlang.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.110-009688?logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Celery](https://img.shields.io/badge/Celery-5.3-green?logo=celery&logoColor=white)](https://docs.celeryq.dev/)
[![Gemini](https://img.shields.io/badge/Google%20Gemini-1.5%20Flash-4285F4?logo=google&logoColor=white)](https://ai.google.dev/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](./LICENSE)

</div>

---

## The Problem

Standard web APIs have a hard limit: if your server doesn't respond within ~30 seconds, the connection is dropped. AI document extraction can easily take 10–30 seconds per file. Naive implementations fail under real-world load.

edocAI solves this with a **an async architecture** — the API responds in ~100ms, and a background worker does the heavy lifting independently.

---

## How It Works

```
User uploads file
       │
       ▼
┌──────────────┐    saves file     ┌─────────────────┐
│   FastAPI    │ ─────────────────▶│ Supabase Storage│
│  (Producer)  │                   └─────────────────┘
│              │    writes PENDING ┌─────────────────┐
│              │ ─────────────────▶│  Neon Postgres  │
│              │                   └─────────────────┘
│              │    pushes job     ┌─────────────────┐
└──────────────┘ ─────────────────▶│  Upstash Redis  │
                                   └────────┬────────┘
                                            │ pulls job
                                            ▼
                                   ┌─────────────────┐
                                   │  Celery Worker  │
                                   │  (Consumer)     │
                                   │                 │
                                   │  1. Download    │
                                   │  2. AI Inference│──▶ Gemini 1.5 Flash
                                   │  3. COMPLETED   │       │ (rate limited?)
                                   └─────────────────┘       ▼
                                                       PyMuPDF + LLM fallback
```

### AI Pipeline & Fallback Router

The worker uses a two-stage fallback to maximize uptime on free-tier rate limits:

| Attempt | Strategy | Trigger |
|---|---|---|
| **1** | Google Gemini 1.5 Flash (vision) | Always tried first |
| **2** | PyMuPDF text extraction + LLM | Only on rate-limit error |

All output is returned as **strictly typed JSON**.

---

## Tech Stack

| Layer | Technology | Purpose |
|---|---|---|
| **Frontend** | Next.js 16, React 19, Tailwind CSS v4 | SaaS UI, SSR, dynamic theming |
| **UI Components** | shadcn/ui, Radix UI | Accessible component primitives |
| **Backend API** | FastAPI (Python 3.11) | RESTful endpoints, OpenAPI docs |
| **Task Queue** | Celery 5.3 | Distributed async workers |
| **Message Broker** | Upstash Redis | Serverless job queue |
| **Database** | Neon (Serverless Postgres) | Managed relational storage |
| **Object Storage** | Supabase Storage | S3-compatible file store |
| **AI Inference** | Google Gemini 1.5 Flash | Multimodal document extraction |
| **Auth** | JWT (Bearer tokens) + bcrypt | Stateless authentication |
| **Frontend Host** | Vercel | Global CDN, zero-config deploy |
| **Backend Host** | Railway | Docker-based, auto-deploy on push |

---

## Security Model

edocAI is built with **multi-tenant isolation** as a first-class concern, not an afterthought.

**Authentication** — Stateless JWTs with Bearer auth. No sessions, no cookies. Every request is independently verified.

**Data Isolation** — Row-Level Security (RLS) is enforced at the PostgreSQL level via `owner_id` foreign keys. Even if a bug exists in the Python logic, users are structurally prevented from accessing each other's documents.

**Password Hashing** — Uses raw `bcrypt` (not `passlib`), which avoids known incompatibilities with some fork/DNS behavior in production environments.

---

## Project Structure

```
edocai/
├── app/                    # Next.js App Router
│   ├── (auth)/             # Login / signup routes
│   ├── dashboard/          # Authenticated SaaS UI
│   └── api/                # Next.js API route handlers
├── components/
│   └── ui/                 # shadcn/ui component library
├── lib/                    # Shared utilities, API client
├── public/                 # Static assets
├── next.config.ts
├── tailwind.config.ts
├── tsconfig.json
└── package.json
```

> **Note:** The FastAPI backend and Celery worker live in a separate repository, deployed independently to Railway.

---

## Local Development

### Prerequisites

- Node.js 20+
- A running instance of the [edocAI backend API](https://github.com/ymahrous/edocai)

### Setup

```bash
# Clone the repository
git clone https://github.com/ymahrous/edocai.git
cd edocai

# Install dependencies
npm install

# Configure environment variables
cp .env.example .env.local
```

Edit `.env.local`:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000   # Your FastAPI backend URL
```

```bash
# Start the development server
npm run dev
```

Open [http://localhost:3000](http://localhost:3000).

---

## Deployment

The full stack deploys to free-tier cloud services with zero configuration.

### Backend (Railway)

1. Connect your GitHub repo to [Railway](https://railway.app).
2. Railway auto-detects the `Procfile` and deploys two services:
   - `web` — the FastAPI server
   - `worker` — the Celery consumer
3. Add environment variables (API keys, DB URLs, Redis URL) in the Railway dashboard.

### Frontend (Vercel)

1. Connect the repo to [Vercel](https://vercel.com).
2. Set `NEXT_PUBLIC_API_URL` to your Railway API URL.
3. Deploy. Vercel handles everything else.

### Environment Variables

| Variable | Required | Description |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | ✅ | Base URL of the FastAPI backend |

---

## Key Engineering Decisions

**Why Celery + Redis instead of threading?**
Python's GIL prevents true parallelism for CPU/IO-bound tasks. Offloading AI inference to a separate Celery process keeps the API non-blocking and allows horizontal scaling of workers independently of the API layer.

**Why raw `bcrypt` instead of `passlib`?**
`passlib` has documented incompatibilities with macOS and certain Linux fork behaviors. The raw `bcrypt` library is lighter, more predictable, and eliminates a class of production surprises.

**Why DB-level RLS instead of application-level filtering?**
Filtering in Python is only as reliable as the code. PostgreSQL RLS is enforced by the database engine itself — it's a hard constraint that survives any application-layer bug.

**Why the Gemini Interactions API?**
The standard REST vision API requires manual base64 encoding, MIME type management, and verbose JSON construction. The Interactions API abstracts this cleanly, keeping the worker code readable and maintainable.

---

## Contributing

Contributions are welcome. Please open an issue first to discuss what you'd like to change.

[CONTRIBUTING GUIDE](./CONTRIBUTING.md)

---

## License

[MIT LICENSE](./LICENSE)

---

<div align="center">

Built with Next.js · FastAPI · Celery · Google Gemini · Railway · Vercel

**[Live Demo →](https://edocai.vercel.app)**

</div>
