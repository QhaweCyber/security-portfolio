# Informal Web Security Check — A Friend's E-Commerce Site

**Author:** Ntokozo Mngomeni — final-year BSc Computer Science student, University of Limpopo. Aspiring SOC analyst.

To be clear upfront: this isn't professional pentest work. I'm a student practicing outside of class, and I'm putting this here because it shows how I actually think through a target — including a couple of dead ends that turned out to be more useful than the actual findings.

**Target:** heavenly-crumbs.vercel.app — a university friend's small scones e-commerce storefront
**Type:** Static Next.js site, hosted on Vercel
**What I looked at:** HTTP headers, directory/file enumeration, login system (if any), checkout flow
**Permission:** Verbal, directly from the site owner — he wanted feedback on hardening his site, I wanted practice
**Tools:** `curl`, `gobuster` + SecLists, browser dev tools, manual poking around

---

## Working out what was actually in scope

Before running anything, I had to think about what "in scope" even meant here. The site's hosted on Vercel, which is shared serverless infrastructure — the actual servers, IPs, and network belong to Vercel, not my friend. His permission covers his own app, not Vercel's infrastructure underneath it.

So a full port scan (`nmap -p-`) was off the table from the start — and honestly wouldn't have made sense anyway, since Vercel serverless sites don't expose normal ports (no SSH, no database port). Everything worth looking at lives at the HTTP/application layer.

## Checking the HTTP headers

```
curl -I https://heavenly-crumbs.vercel.app
```

`strict-transport-security` was set correctly (`max-age=63072000; includeSubDomains; preload`) — solid config. But `content-security-policy`, `x-frame-options`, and `x-content-type-options` were all missing, so there's no clickjacking protection and no MIME-sniffing protection. `access-control-allow-origin` was set to `*`, which isn't really a problem for a plain storefront with no API, but would need tightening if authenticated endpoints get added later.

The response headers also gave away the stack (Next.js App Router, server-rendered through Vercel's edge cache), which was useful context going forward.

## Directory scanning — and a false-positive I almost missed

Ran gobuster against the site with SecLists' common wordlist:

```
gobuster dir -u https://heavenly-crumbs.vercel.app -w /usr/share/seclists/Discovery/Web-Content/common.txt
```

At first glance the results looked bad — about 4,750 requests, almost all coming back as 403, and all roughly the same size (~33.8KB), even for paths that obviously shouldn't exist. That pattern is usually a red flag that you're not looking at real findings — you're looking at one generic block page being served for everything.

I checked manually with `curl -Iv` against one of the flagged paths (`.git/logs/`) and got back:

```
x-vercel-mitigated: challenge
```

So Vercel's own bot-mitigation system had picked up the scan and started blanket-blocking everything after that. Which is actually a good sign for my friend's site — his firewall is doing its job — but it also meant there was nothing more to find through directory scanning.

**What I took from this:** a wall of identical-looking "hits" usually means something is blocking you, not that you've found a thousand real files. Worth manually checking anomalies before trusting tool output at face value.

## Login system and checkout

Tried the obvious routes — `/login`, `/signin`, `/account`, `/auth/login` — all came back 404. So there's no user account system at all; it's a purely static storefront. Checkout happens through a WhatsApp link rather than any real payment flow on the site itself. That means authentication testing (brute-force protection, session cookies, etc.) just doesn't apply here — and I confirmed that by actually testing the routes rather than assuming.

## What I found, overall

Transport security was solid. A few standard security headers were missing. CORS is loose but not really a problem yet. No exposed directories (scanning got blocked at the platform level before finding anything real). No login system to test. Payment happens off-site through WhatsApp.

## What I learned from this

Testing a site hosted on Vercel is not the same as testing a normal server. There's no ports to scan, so most of the work happens at the website level instead — things like headers and how the app responds. I also learned that just running a tool isn't enough — when gobuster gave me a bunch of results, I had to actually check if they were real or just Vercel blocking me. That mattered more than running extra scans. Lastly, instead of just guessing that there was no login page, I actually tested the login links myself to be sure.
