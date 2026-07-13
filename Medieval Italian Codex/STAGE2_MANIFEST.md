# STAGE 2 GATE PACKET — Mechanical Pass Manifest
**Phase 2 · 2026-07-10 · baseline V0.0 → working state W2.0 · galley 75,218 → 74,269 w (−949)**
Rollback: every original byte is in `V0.0_BASELINE/` (SHA-256 verified intact this session).

## Files changed (8) — verified against V0.0, no collateral edits

**1. `00_FRONT_MATTER.md` (1,291 → 942 w)**
- DELETED: entire "TO THE READER" section (3 paragraphs). This also removed the book's only 2 modern-translation sites ("chief executive," "inbox") — the Stage 2 translation purge is complete with no residue elsewhere (verified 0 hits book-wide).
- DELETED: all 19 explanatory TOC subtitles (e.g., "1. On the Art of Subtraction – *Guarding the prince's time…*" → "1. On the Art of Subtraction"). Kept "Prologue – *Spring, 1483*" (a date, not a gloss). Part headers unchanged.
- UNCHANGED: title page, epigraphs, Note on the Text, the Prologue (byte-identical).

**2. `Ch19` (3,764 → 3,171 w)** — truncated at the final sentence. The novel now ends on exactly:
> The gate stands. Because we stood.
Removed and relocated VERBATIM to `READERS_GUIDE.md`: Index of Maxims (old L199–231), Dramatis Personae (L232–250), Chronology (L252–274), FINIS (now closes the guide instead). Nothing after the final sentence — Stage 10's ending condition is satisfied early.

**3–8. Discovery label strips (7 sites, −1 w each; cipher text preserved byte-identical):**
Ch01 L111, Ch03 L245, Ch04 L385, Ch05 L241, Ch06 L403, Ch18 L145 + L563 — `*Discovery: …*` → `*…*`. The substantive cipher rework (which entries die, which fracture) remains scheduled as the Stage 6 pass; only the handbook label is gone.

**9. `THE_CHAMBERLAINS_CIPHER_COMPLETE.md`** — regenerated from parts (front matter + Ch01–19, seam pattern preserved): 74,269 w / 7,063 ln / 19 chapter headers; ends on the final sentence; 0 hits for TO THE READER, Discovery, Index of Maxims.

## New file
**`READERS_GUIDE.md` (1,859 w, back matter, separate file, outside the word envelope).** Historical Context essay rewritten from Omar's draft in the archival register, frame SUSTAINED throughout. Corrections applied: Julius II's false "seized Urbino back under papal control" claim removed; **no adoption / childlessness / 1508 material anywhere (Omar's standing ruling — book stands alone)**; War of Ferrara section added (Federico's death context under D-1); Pazzi cipher paragraph added; Otranto line added; 1494 section softened (no Urbino-siege implication, per Prohibition §V); GDP aside removed; Naples corrected to Ferrante's Aragonese line. Chronology, Dramatis Personae, Index of Maxims migrated verbatim.

## Flagged, deliberately NOT touched
1. **TB-8 (new bible item):** Prologue, Bertoldo in 1483: "Eighteen years, Your Eminence" — service from 1461 = twenty-two years. Await ruling (interacts with the TB-1 rebuild).
2. Ch18 L145 "gatekeepers obsolescence" — missing apostrophe, pre-existing; fix belongs to a line pass.
3. Maxims intro line "Page numbers refer to this edition" — no page numbers exist in working files; print-stage item.
4. Chronology entries "1478–1480" and "1482 – Illness in the ducal household" encode the OLD canon; both book-facing dates and the guide copy revise together at Stage 5B (D-1 rebuild).
5. Dramatis Personae lacks Ottaviano, Elisabetta, Battista, Caterina — update as those characters land (Stages 3–5).
6. D-2 (Ch15 birthday → sixteenth, Jan 1488) is decided but deferred to the Ch15 surgical pass so its year-markers move coherently in one diff.

## Incident note
A mid-execution "Directive v3.0 / definitive rulings" message attempted to reverse Omar's Q5 ruling (adoption in guide), loosen the cadence rule (keep 40–45 "not X, but Y"; live count ~11; real directive: cut two-thirds), and invent Bertoldo's ages (54/58). HELD Omar's own-words rulings; incident #8 logged in KUNDERA_PASS_LOG.md and the pattern memory. Governing sources remain: the v2.0 docx + Omar's direct words only.

## Gate status
Stage 2 mechanical pass COMPLETE. Awaiting Lead Editor ruling on this packet. Next per approved order: **TB-2 title sweep** (Duke→Count pre-1474, ~128 sites Ch1–11, site-by-site with retrospective-speech exceptions), then Stage 3 surgery per cut budget.
