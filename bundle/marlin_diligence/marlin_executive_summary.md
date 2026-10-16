# Executive Summary

## Meridian Federal Systems, Inc. Due Diligence — CMMC v2 Level 2

**Prepared for:** Bayline Capital Partners\
**Prepared by:** Chris McConnell, Eagle Ridge Advisory\
**Report Date:** October 1, 2025

*This is an anonymized client report stripped of identifying data. The insights and methodology are consistent with the approach Eagle Ridge takes doing technology due diligence with M&A partners.*

---

## EXECUTIVE SUMMARY

### Transaction Overview
Bayline Capital Partners is evaluating the acquisition of Meridian Federal Systems, Inc. (MFS), a government contractor with $103.2M in contract backlog. This diligence report assesses MFS's current CMMC v2 Level 2 compliance posture and quantifies the financial impact of remediation requirements on the proposed transaction.

### Key Findings

**Compliance Posture: HIGH RISK**

MFS currently maintains a **partially non-compliant** CMMC v2 Level 2 environment with **critical control deficiencies** that directly threaten contract eligibility and revenue realization. The company has documented 18 open POA&M items, including multiple HIGH-severity gaps in gating controls. The current SPRS score of **76 is 12 points below the minimum threshold of 88** (80% compliance) typically required to pass a CMMC Level 2 assessment, and **34 points short of the 110 maximum score** representing full NIST 800-171 compliance. This 69% compliance rate (76/110) indicates systemic gaps across multiple control families, not merely isolated deficiencies.

**Revenue at Risk:**

- **Total Contract Backlog:** $103,205,606
- **CMMC-Dependent Revenue:** 95%+ of backlog (estimated $96.9M-$102.6M)
- **Immediate Risk Contracts:** Minimum $57M+ in DoD/Federal contracts requiring CMMC Level 2 certification

**Critical Control Deficiencies (Gating Issues):**

| Control | Practice | Score | Risk Level | Revenue Impact |
|---------|----------|-------|------------|----------------|
| 3.5.3 | Multifactor Authentication | 0/5 | **CRITICAL** | Eligibility blocker |
| 3.1.18 | Mobile Device Connection | 0/5 | **HIGH** | CUI leakage risk |
| 3.1.19 | Encrypt CUI on Mobile | 0/3 | **HIGH** | CUI leakage risk |
| 3.5.6 | Identifier Disablement | TBD | **MEDIUM** | Unauthorized access |
| 3.8.x | Media Protection | TBD | **MEDIUM** | Incomplete CUI handling |
| 3.1.20 | External Connections | 1/1* | **MEDIUM** | Needs hardening |

*Score marked "implemented" but SSP notes "needs improvements"


### Financial Impact Summary

**Cost to Cure (Post-Closing Investment Required):**

- **Initial Remediation (Months 1-6):** $741,000 - $1,140,000
- **Year 1 Operating Expenses:** $205,000 - $262,000
- **Years 2-5 Operating Expenses:** $365,000 - $513,000 annually (1.6-2.3% of revenue)

**Total 5-Year Compliance Investment:** $2.4M - $3.4M

**EBITDA Impact:**

- Year 1: ($946K - $1.4M) one-time + recurring
- Years 2-5: ($365K - $513K) annually

**Why the investment is worth it:**
The $2.4M-$3.4M compliance investment over 5 years preserves access to $96.9M+ in current backlog and enables pursuit of the expanding CMMC-mandated DoD contract market. Without it, an estimated $57M+ of gated contracts becomes unwinnable as CMMC enforcement reaches award and option dates.

### Investment Implications

**For Private Equity (Bayline Capital Partners):**

1. **Immediate Capital Call:** Allocate $741K-$1.14M in working capital for Day 1 remediation
2. **EBITDA Adjustment:** Budget permanent margin compression of 1.6-2.3% of revenue for ongoing compliance
3. **Timeline Risk:** 6-12 month remediation period may impact option year exercises and recompetes
4. **Exit Considerations:** CMMC compliance becomes a value driver for strategic buyers or add-on acquisitions

**For SBIC Lender:**

1. **Liquidity Requirements:** Structure $1.14M draw facility for compliance CapEx within first 6 months
2. **Cash Flow Coverage:** Recurring $365K-$513K OpEx reduces debt service capacity
3. **Covenant Structuring:** Link compliance milestones to borrowing availability or amortization schedules
4. **Revenue Concentration Risk:** 95%+ of backlog depends on maintaining CMMC certification

### Recommendation

**PROCEED WITH TRANSACTION** subject to the following conditions:

1. **Escrow Holdback:** Retain $1.1M of purchase price in escrow pending completion of MFA (3.5.3) and Intune deployment (3.1.18, 3.1.19)
2. **Post-Closing Remediation Plan:** Seller to provide detailed implementation roadmap with defined milestones within 30 days of close
3. **GCC Migration Contingency:** Validate Microsoft GCC eligibility and pricing prior to close; budget may increase if GCC High is required
4. **Working Capital Adjustment:** Increase working capital target by $1.14M to fund immediate remediation
5. **Rep & Warranty Package:** Obtain robust cybersecurity insurance with CMMC-specific coverage ($5.7M minimum)

