# Informal Web Security Assessment — Student E-Commerce Site

**Author:** Ntokozo Mngomeni — final-year BSc Computer Science student, University of Limpopo. Aspiring SOC analyst.

> **Context:** This isn't professional pentest work — I'm a student building hands-on skills outside the classroom. I'm including this to show how I approach a real target: scoping it properly, reading tool output critically, and adjusting when something doesn't go as expected. Feedback welcome.

## Overview

A lightweight, authorized security review of a small Next.js e-commerce storefront, conducted informally with the site owner's permission as a mutual learning exercise between students. The owner (a fellow student developer) wanted feedback on hardening the site; I wanted hands-on practice applying reconnaissance and assessment techniques to a real, live target.

This write-up focuses as much on **process and reasoning** as on findings — including a couple of dead ends that were themselves useful lessons.

**Target:** heavenly-crumbs.vercel.app — a university friend's small scones e-commerce storefront
**Target type:** Static Next.js storefront, deployed on Vercel
**Scope:** HTTP header analysis, directory/file enumeration, authentication surface, checkout flow
**Authorization:** Informal, verbal, granted directly by the site owner/developer
**Tools used:** `curl`, `gobuster` + SecLists, browser DevTools, manual review

---

## 1. Scoping the engagement correctly

Before touching any tooling, the target's hosting model changed what was actually in scope. The site is deployed on **Vercel**, a shared serverless platform — meaning the underlying infrastructure (IP, load balancer, edge network) is Vercel's, not the site owner's. The owner's authorization covers their own application, but cannot extend to Vercel's shared servers.

**Practical consequence:** a full port scan (`nmap -p-`) was ruled out entirely. Vercel serverless deployments don't expose traditional ports anyway (no SSH, no database port) — the entire attack surface lives at the HTTP/application layer. This scoping decision shaped the rest of the assessment.

## 2. HTTP header review

```
curl -I https://heavenly-crumbs.vercel.app
```

| Header | Status | Note |
|---|---|---|
| `strict-transport-security` | ✅ Present | `max-age=63072000; includeSubDomains; preload` — strong config |
| `content-security-policy` | ❌ Missing | No script-source restrictions |
| `x-frame-options` | ❌ Missing | Clickjacking not mitigated |
| `x-content-type-options` | ❌ Missing | MIME-sniffing not blocked |
| `access-control-allow-origin` | ⚠️ `*` | Fine for a static storefront today; would need scoping down if authenticated APIs are added later |

Response headers also revealed the tech stack (Next.js App Router, server-rendered via Vercel edge cache) — useful context for the rest of the assessment.

## 3. Directory/file enumeration — and a false-positive lesson

Ran `gobuster` against the target using SecLists' common wordlist:

```
gobuster dir -u https://heavenly-crumbs.vercel.app -w /usr/share/seclists/Discovery/Web-Content/common.txt
```

Initial results looked alarming: **4,750 requests, nearly all returning 403** with near-identical response sizes (~33.8KB), including for obviously nonsensical paths. This is a classic signal that the results are **noise, not findings** — a single blanket response being served for everything, not thousands of real hidden files.

Manually verifying with `curl -Iv` against the flagged `.git/logs/` path confirmed it:

```
x-vercel-mitigated: challenge
```

Vercel's bot-mitigation system had detected the automated scan and started serving a uniform challenge/block page for all subsequent requests. **The scan itself became the finding** — it confirmed Vercel's edge firewall is active and correctly identifying scripted traffic, which is a positive security signal for the site owner, even though it made further directory enumeration pointless.

**Lesson:** a wall of identical-looking "hits" is a stronger signal of a blocking mechanism than of real exposure. Always spot-check anomalous results manually before treating tool output as ground truth.

## 4. Authentication and checkout surface

No login/signup routes exist (`/login`, `/signin`, `/account`, `/auth/login` all returned 404) — this is a purely static storefront with no user accounts. Checkout is handled via a WhatsApp deep link rather than a server-side order/payment flow.

**Consequence for scope:** authentication testing (enumeration, brute-force protection, session cookie flags) does not apply to this site as currently built. This was confirmed rather than assumed, by directly testing the expected routes.

## 5. Summary of findings

| Category | Result |
|---|---|
| Transport security | Strong (HSTS configured correctly) |
| Security headers | Missing CSP, X-Frame-Options, X-Content-Type-Options |
| CORS | Overly permissive (`*`), non-issue today, worth revisiting if the app grows |
| Directory exposure | None found; scan blocked by platform-level bot mitigation |
| Authentication | Not present; not applicable to current scope |
| Payment handling | Out of scope — occurs off-platform via WhatsApp |

## Takeaways

- Recon on modern platforms (Vercel, Netlify, similar) requires adjusting assumptions from traditional infrastructure pentesting — no ports, but real edge-layer protections to account for.
- Reading tool output critically (recognizing the gobuster false-positive flood) mattered more here than running more tools.
- Confirming scope by testing rather than assuming (checking real auth routes instead of guessing) kept the assessment honest and accurate.
