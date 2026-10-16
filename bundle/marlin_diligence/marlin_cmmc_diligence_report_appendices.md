# Meridian Federal Systems Due Diligence Report, Appendices (continued from marlin_cmmc_diligence_report.md)

## APPENDICES

### Appendix A: SSP Gap Detail Matrix

*(See separate file: `Appendix_A_SSP_Gap_Matrix.xlsx`)*

**Contents:**

- Line-by-line SSP control review (110 controls)
- Compliance scores (0/5 to 5/5)
- Gap descriptions
- Remediation recommendations
- Cost estimates by control

---

### Appendix B: Contract Backlog Tables

**Table B.1: Top 20 Contracts by Backlog Value**

| Rank | Contract # | Customer | Project | Backlog | CMMC Risk |
|------|------------|----------|---------|---------|-----------|
| 1 | 902198 | Questar Systems | ANC VOS III | $23,801,113 | HIGH |
| 2 | 902182 | GDIT | Justified | $24,636,351 | MEDIUM |
| 3 | 902183 | FDIC | FDIC III | $12,877,635 | MEDIUM |
| 4 | 902195 | DHS CISA | Escort Services II | $9,767,029 | HIGH |
| 5 | 902178 | AF | COMSEC Allied Partner Nation A MOD | $5,424,990 | HIGH |
| ... | ... | ... | ... | ... | ... |

*(Full table in separate file: `Appendix_B_Contract_Backlog.xlsx`)*


### Appendix C: Cost Model Assumptions

**Table C.1: Initial Remediation Cost Breakdown**

| Line Item | Unit Cost | Quantity | Total Low | Total High |
|-----------|-----------|----------|-----------|------------|
| MFA Licensing (Entra ID P1) | $7/user/mo | 50 users × 12 mo | $4,100 | $4,100 |
| Hardware Tokens (YubiKey) | $57/token | 10 admin users | $570 | $570 |
| MFA Deployment Services | $170/hr | 200-300 hours | $34,200 | $51,300 |
| User Training (MFA) | $2,300/session | 5 sessions | $11,400 | $11,400 |
| Authenticator Apps (Duo backup) | $3/user/mo | 50 users × 12 mo | $2,050 | $4,100 |
| Contingency (10%) | | | $5,150 | $7,200 |
| **MFA Total** | | | **$57,470** | **$78,670** |

*(Full cost model in separate file: `Appendix_C_Cost_Model.xlsx`)*

---

### Appendix D: POA&M Tracker

**Table D.1: Open POA&M Items with Status**

| POA&M ID | Control | Severity | Scheduled Completion | Status | Blocker |
|----------|---------|----------|----------------------|--------|---------|
| MFS-0325-001 | 3.1.3 (CUI Flow) | HIGH | TBD | Not Started | GCC Migration |
| MFS-0325-002 | 3.1.18 (Mobile Device) | HIGH | TBD | Not Started | Intune Deployment |
| MFS-0325-003 | 3.1.19 (Mobile Encryption) | HIGH | TBD | Not Started | Intune Deployment |
| MFS-0325-004 | 3.4.7 (Wireless) | MEDIUM | TBD | In Progress | Firewall Upgrade |

*(Full POA&M tracker in separate file: `Appendix_D_POAM_Tracker.xlsx`)*

---

### Appendix E: Risk-Adjusted Backlog Waterfall

**Chart E.1: Backlog Realization Under CMMC Scenarios**

```
Gross Backlog: $103.2M
├─ Near-Term Funded (0-12 mo): $39.9M [100% probability] → $39.9M
├─ Mid-Term Option Years (12-24 mo): $34.2M [50% probability] → $17.1M
└─ Long-Term Unfunded (24+ mo): $29.1M [40% probability] → $11.6M

Risk-Adjusted Backlog: $68.6M
Risk-Adjustment Haircut (gross $103.2M - risk-adjusted $68.6M): $34.5M
```

*(Full waterfall model in separate file: `Appendix_E_Backlog_Waterfall.xlsx`)*

---

### Appendix F: Remediation Timeline Gantt Chart

*(See separate file: `Appendix_F_Remediation_Gantt.pdf`)*

**High-Level Milestones:**

- **Month 1:** MFA Deployed
- **Month 2:** GCC Migration Complete
- **Month 3:** Intune MDM Operational
- **Month 4:** Firewall & Network Hardened
- **Month 6:** All POA&Ms Closed
- **Month 9:** C3PAO Assessment Complete
- **Month 10:** CMMC Level 2 Certified

---

### Appendix G: Glossary of Terms

| Term | Definition |
|------|------------|
| **C3PAO** | Certified Third-Party Assessment Organization (conducts CMMC audits) |
| **CDI** | Covered Defense Information (legacy term, now subsumed under CUI) |
| **CMMC** | Cybersecurity Maturity Model Certification (DoD cybersecurity framework) |
| **CUI** | Controlled Unclassified Information (sensitive but unclassified federal data) |
| **DFARS** | Defense Federal Acquisition Regulation Supplement (DoD contract clauses) |
| **DSCR** | Debt Service Coverage Ratio (EBITDA ÷ debt payments) |
| **GCC** | Government Community Cloud (Microsoft's government-focused cloud environment) |
| **MDM** | Mobile Device Management (software to manage/secure mobile devices) |
| **MFA** | Multifactor Authentication (login security requiring 2+ verification factors) |
| **MSSP** | Managed Security Service Provider (outsourced SOC/monitoring) |
| **NIST 800-171** | National Institute of Standards and Technology Special Publication 800-171 (basis for CMMC Level 2) |
| **POA&M** | Plan of Action & Milestones (document tracking compliance gaps) |
| **SBIC** | Small Business Investment Company (SBA-licensed lender for small business acquisitions) |
| **SIEM** | Security Information and Event Management (log aggregation and threat detection platform) |
| **SPRS** | Supplier Performance Risk System (DoD portal for self-reporting NIST 800-171 scores) |
| **SSP** | System Security Plan (comprehensive documentation of security controls) |

---

### Appendix H: Sources & References

**Primary Documents Reviewed:**

| # | Document Type | File Name | Date | Source | Key Content |
|---|--------------|-----------|------|--------|-------------|
| 1 | System Security Plan (SSP) | SSP - Meridian Federal Systems, Inc.pdf (165 pages) | Not specified | Transaction advisors | CMMC v2 Level 2 control assessment (ISI prepared) |
| 2 | Plan of Action & Milestones | MFS POAM 3.24.2025.xlsx | Mar 24, 2025 | Transaction advisors | 18 control deficiencies with severity ratings |
| 3 | Contract List | Contract List 5.31.csv | May 31, 2025 | Transaction advisors | 33 active contracts, $103.2M total backlog |
| 4 | Contract Waterfall | Contract Waterfall Completed.xlsx | Not specified | Transaction advisors | Revenue projection, funded/unfunded segmentation |
| 5 | Mitigation Response | Mitigation Response_9X4R2 MFS 20240529 FCS.pdf | May 29, 2024 | Transaction advisors | Compliance context and mitigation strategies |

**Public Sources:**

| # | Source | URL | Date Accessed | Key Information |
|---|--------|-----|---------------|-----------------|
| 6 | SAM.gov Entity Registration | https://sam.gov/entity/FZ7QPX3RT9K2 | Oct 1, 2025 | MFS: UEI FZ7QPX3RT9K2, CAGE 9X4R2 |
| 7 | MFS Corporate Website | https://meridianfederalsystems.com | Oct 1, 2025 | Serves US Intelligence/Defense communities, SDVOSB, founded 2006 |
| 8 | Vantage Point Consulting (CMMC Consultant) | https://vantagepointdefense.com | Oct 1, 2025 | RPO but not authorized C3PAO |
| 9 | Third-Party Contractor Databases | GovTribe, HigherGov | Oct 1, 2025 | Historical awards, classification validation |

**Regulatory References:**

| # | Regulation | Published | Authority | Key Content |
|---|-----------|-----------|-----------|-------------|
| 10 | CMMC 2.0 Final Rule | Oct 2024 | DoD CIO (dodcio.defense.gov/CMMC/) | Certification requirements, phased timeline, C3PAO rules |
| 11 | NIST SP 800-171 Rev 2 | Feb 2020 | NIST (csrc.nist.gov) | 110 security controls (CMMC Level 2 basis) |
| 12 | DFARS 252.204-7012 | Current | Defense FAR Supplement | DoD contractor cybersecurity requirements |
| 13 | 32 CFR Part 2002 | Current | Code of Federal Regulations | CUI handling, marking, breach notification |

**Industry Cost Benchmarks:**

| # | Benchmark | Sources | Typical Range | Estimate Applied to MFS |
|---|-----------|---------|---------------|-------------------------|
| 14 | CMMC Compliance Costs | Coalfire, CyberSheath, NDIA | $570K-$1.1M initial + 1.5-3.0% revenue annually | $741K-$1.14M initial, $205K-$262K Y1, $365K-$513K Y2-5 |
| 15 | Microsoft GCC High Pricing | Microsoft Gov Cloud docs | 2.0-2.5x commercial O365 | $137K-$228K annually (~50 users; external benchmark -- Appendix C models a ~$43K-$47K/yr uplift) |

**Subject Matter Expert Consultation:**

This report was prepared by Chris McConnell, Eagle Ridge Advisory, with expertise in:

- CMMC v2 compliance assessment and remediation planning
- Government contractor cybersecurity and risk management
- M&A due diligence for defense industrial base companies
- Financial modeling for compliance investment ROI

**Data Analysis Methods:**

- Contract backlog risk segmentation based on CMMC timing requirements (near-term, mid-term, long-term)
- SPRS score gap analysis: 76 current vs. 88 threshold vs. 110 maximum
- Cost-to-cure modeling with 5-year NPV analysis
- Risk-adjusted expected value calculations using probability-weighted scenarios
- Debt service coverage ratio (DSCR) impact modeling for SBIC lender underwriting

**Limitations:**

- SSP and POA&M documents were reviewed but not independently validated through hands-on technical assessment
- Contract classification levels not confirmed (DD Form 254s not provided during diligence)
- Facility Clearance Letter (FCL) not provided; classification level inferred from contract portfolio
- Microsoft environment (Commercial vs. GCC vs. GCC High) not confirmed; GCC High requirement inferred from COMSEC/IC work
- SPRS score of 76 reported but not independently validated through SPRS portal access
- Cost estimates based on industry benchmarks; actual costs may vary based on vendor selection and implementation complexity

**Recommendations for Further Diligence:**

1. Request and review MFS's current SPRS assessment (screenshot or export from SPRS portal)
2. Obtain Facility Clearance Letter (FCL) from DCSA to confirm classification level
3. Collect DD Form 254s for all COMSEC and IC contracts
4. Validate current Microsoft environment (Commercial, GCC, or GCC High)
5. Interview Dana Ellis (IT Director) and Vantage Point Consulting for remediation timeline validation
6. Engage independent C3PAO for pre-assessment gap validation (budget $6K-$11K)
7. Request cyber liability insurance quotes with CMMC-specific coverage

---

**END OF REPORT**


**Document Control:**

- **Version:** 1.0 Draft
- **Date:** October 1, 2025
- **Classification:** CONFIDENTIAL - For Bayline Capital Partners Internal Use Only
- **Distribution:** Limited to Investment Committee, SBIC Lender, and Transaction Advisors

**Disclaimer:** This report is based on review of documents provided as of the report date. It does not constitute a full C3PAO assessment and should not be relied upon as a guarantee of CMMC certification outcomes. Bayline Capital Partners should engage qualified CMMC professionals for definitive certification roadmap.
