# Tidewater Biologics LLC — engagement profile (generated stand-in)

This organization is fictional. It mirrors the shape of a real three-person
biotech engagement: same team size, same device mix, same contract instrument
question, same control statuses. Every name, address, number, and date below is
invented. The control statuses in `tidewater_control_register.yaml` are the
real engagement's statuses and are the ground truth for scoring tasks.

## Company

- Legal name: Tidewater Biologics LLC
- What they do: marine-derived biomaterials research for a Navy sponsor
- Location: single leased lab and office suite, 410 Harbor Point Rd, Suite 2B, Wilmington NC
- Headcount: 3
  - Dr. Priya Raman, co-founder and CEO. Only person authorized to access CUI. Also the de facto IT administrator.
  - Jonah Whitfield, project scientist. No CUI access.
  - Ines Marchetti, research associate, non-US person (permanent resident). No CUI access. Access is restricted by policy and Google Workspace organizational unit, not by network segmentation.
- Registered in SAM.gov, active. CAGE and UEI on file (redacted from this bundle).

## Award

- Sponsor: Office of Naval Research, BAA-derived award
- Award number: N0001426C0417 (fictional, N00014-series format)
- Instrument type: CONTRACT, confirmed on the intake call after a two-week period where the team believed it was a grant
- Clauses present: DFARS 252.204-7012, 7019, 7020, 7021
- CMMC requirement: Level 2, self-assessment. No C3PAO certification required. SPRS posting plus annual affirmation.
- Engagement: SSP plus SPRS score, fixed fee, six weeks, Feb 24 to Apr 8, 2026

## System boundary as agreed on the intake call

- Google Workspace Business Plus, upgraded to Enterprise Plus with Assured Controls during the engagement (US data residency, access transparency)
- Three laptops: two MacBook Air (macOS 14.6), one Lenovo IdeaPad 5 (Windows 11 Home)
- One lab workstation not connected to the CUI boundary
- Team chat (Slack free tier) excluded from the CUI boundary by written policy: no CUI in chat
- Mobile phones excluded from the CUI boundary by written policy dated 2026-03-19: no phone stores, processes, or transmits CUI. Controls 3.1.18 and 3.1.19 are marked N/A on that basis.
- No on-premises servers, no VPN, consumer router in the suite

## What the assessment found (v0.5, 2026-03-25)

- 15 controls MET, 2 N/A, 4 PARTIAL, 89 NOT MET
- The MET controls cluster in Identification and Authentication (MFA on Google Workspace covers 3.5.3 in full) and three System and Communications Protection controls
- Two of the four PARTIAL controls (3.1.1 and 3.1.2) receive no partial credit under the DoD methodology and deduct their full 5 points each
- 3.13.11 PARTIAL: encryption is in use but not FIPS 140-2 validated. This is one of the two controls with a 3-point partial deduction, and it is POA&M eligible.
- 3.12.4 PARTIAL: SSP in draft. Zero-point control, but it is not POA&M eligible and blocks conditional status until the SSP exists.
- 3.12.2 MET: the POA&M produced in this engagement is itself the artifact that satisfies the control. This was reclassified from NOT MET late in the engagement and moved the SPRS score by 3 points.

## Owner's words on what good and bad look like

- "I need to know which of these 89 gaps I can put on a plan and which ones I have to fix before I post a score."
- "Last time someone gave us a percentage. The Navy portal does not take a percentage."
- "Do not tell me to buy a SIEM. There are three of us."
- The reviewer rejected a draft narrative that said "will implement" for a control marked MET, and another that pasted the NIST requirement text back as the implementation.
