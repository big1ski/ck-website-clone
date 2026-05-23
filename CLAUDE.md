# CLAUDE.md — Project Rules

## Always Do First
- Read `PROJECT_BRIEF.md` in full at the start of every session — it defines what we're building.
- Invoke the `frontend-design` skill before writing any frontend code, every session, no exceptions.

## Project Context
This is a personal graduation website hosted on GitHub Pages at a custom `.me` domain.
Multi-page static site: a landing page (`index.html`) plus optional subpages
(Gallery, About). Plain HTML/CSS with light JavaScript. Tailwind CSS via CDN is
acceptable if it helps. No heavy build chain, no frameworks.

## Local Server
- Always serve on localhost — never screenshot a `file:///` URL.
- If a `serve.mjs` or equivalent doesn't exist, create one and place it in the project root,
  serving the root at `http://localhost:3000`.
- Start the dev server in the background before screenshots. Don't start a second instance
  if one is already running.

## Screenshot Workflow (when verifying design)
- Set up Puppeteer for screenshot capture if not already present, with macOS-appropriate paths.
- Always screenshot from `http://localhost:3000`, never from a local file URL.
- Save screenshots to `./temporary-screenshots/screenshot-N.png` (auto-incremented).
- After screenshotting, read the PNG and analyze it directly.
- Compare specifically: spacing/padding (exact px), font size/weight/line-height,
  colors (exact hex), alignment, border-radius, shadow treatment, image sizing.
- Do at least 2 compare-and-fix rounds. Stop only when no visible mismatches remain
  or I tell you to stop.

## Reference Images
- If I provide a reference image (Figma export, screenshot, mood board): match layout,
  spacing, typography, and color exactly. Use placeholders for content
  (images via `https://placehold.co/`, generic copy). Don't improve or add to the design.
- If no reference: design from scratch using the anti-generic guardrails below.

## Output Defaults
- Multi-page static site: `index.html`, plus subpages as needed (e.g. `gallery.html`, `about.html`).
- Tailwind CSS via CDN is acceptable: `<script src="https://cdn.tailwindcss.com"></script>`.
- Placeholder images: `https://placehold.co/WIDTHxHEIGHT`.
- Mobile-first responsive: design for ≤390px first, enhance for desktop.

## Brand Assets
- Check the `brand_assets/` folder before designing (create it if missing). It may contain
  logos, color guides, or images. If assets exist there, use them — don't use placeholders
  where real assets exist. If a color palette is defined in the brief or assets, use those
  exact values — don't invent.

## Anti-Generic Guardrails
- **Colors:** Never use default Tailwind palette (indigo-500, blue-600, etc.). Pick a custom
  palette derived from the brief's three tones (warm off-white, deep navy, gold accent).
- **Shadows:** Never flat `shadow-md`. Use layered, color-tinted shadows with low opacity.
- **Typography:** Never the same font for headings and body. Pair a display/serif with a
  clean sans. Tight tracking (`-0.03em`) on large headings, generous line-height (`1.7`) on body.
- **Gradients:** Layer multiple radial gradients. Add grain/texture via SVG noise filter for depth.
- **Animations:** Only animate `transform` and `opacity`. Never `transition-all`. Spring-style
  easing. Respect `prefers-reduced-motion` — disable non-essential motion when set.
- **Interactive states:** Every clickable element needs hover, focus-visible, and active states.
- **Images:** Add a subtle gradient overlay and a color treatment layer where appropriate.
- **Spacing:** Use intentional, consistent spacing tokens — not random Tailwind steps.
- **Depth:** Layering system (base → elevated → floating), not all surfaces at the same z-plane.

## Hard Rules
- Don't add sections, features, or content not in `PROJECT_BRIEF.md` or in a provided reference.
- Don't "improve" a reference design — match it.
- Don't stop after one screenshot pass.
- Don't use `transition-all`.
- Don't use default Tailwind blue/indigo as primary color.
- Don't commit or push to git unless I explicitly ask.