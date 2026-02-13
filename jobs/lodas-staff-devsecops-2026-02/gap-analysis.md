---
candidate: "Thomas (Tom) James Robison"
position: "Staff DevSecOps Engineer"
company: "LODAS"
analysis_date: "2026-02-13"
overall_match: "38.4%"
recommendation: "CONSIDER WITH CAVEATS"
---

# Gap Analysis: Staff DevSecOps Engineer at LODAS

## Executive Summary

**Overall Assessment:** MODERATE FIT with significant transferable skills but notable technical gaps

**Match Score:** 38.4% (31.0% required keywords, 55.6% preferred keywords)

**Key Strengths:**
- ✅ Exceptional security and compliance expertise (SOC 2, NIST, FedRAMP, HIPAA)
- ✅ Extensive AWS operations at scale (100+ server migration, 10M+ users)
- ✅ Strong leadership and technical mentorship background
- ✅ Multi-director experience (DevOps, Security, Compliance, IT)

**Key Gaps:**
- ❌ No documented Terraform experience (uses Chef + CloudFormation)
- ❌ No GitHub Actions experience (uses Jenkins)
- ❌ Limited serverless stack experience (ECS Fargate, Lambda, SQS, Aurora)
- ❌ No Vanta compliance platform experience

**Recommendation:** Consider applying if willing to emphasize transferable IaC and CI/CD skills, but be prepared to demonstrate rapid learning ability for the modern serverless stack.

---

## Detailed Gap Analysis

### 1. Core Requirements Analysis

| Requirement | Candidate Experience | Match Level | Gap Analysis |
|-------------|---------------------|-------------|--------------|
| **6+ years DevOps/SRE experience** | 10+ years (2014-present) | ✅ STRONG MATCH | Exceeds requirement significantly |
| **Deep AWS experience** | AWS (EC2, RDS, S3, IAM, CloudWatch, CloudFormation) | ⚠️ PARTIAL MATCH | Has AWS but not the specific serverless stack (ECS Fargate, Lambda, SQS, Aurora) |
| **Multi-account AWS environments** | Managed AWS infrastructure but multi-account strategy not documented | ⚠️ PARTIAL MATCH | Has AWS ops experience but multi-account specifics unclear |
| **Terraform expertise** | Uses Chef and CloudFormation, not Terraform | ❌ GAP | Different IaC tool; transferable but not identical |
| **GitHub Actions CI/CD** | Jenkins CI/CD expertise | ⚠️ TRANSFERABLE | Different CI/CD platform; concepts transfer |
| **Security/compliance integration** | Extensive (NIST, FedRAMP, SOC 2, HIPAA, Nessus, Splunk) | ✅ STRONG MATCH | Major strength; exceeds requirement |
| **Vanta compliance platform** | No documented experience | ❌ GAP | No experience with this specific tool |
| **Python/Bash scripting** | Python, Bash, Ruby | ✅ MATCH | Meets requirement |
| **Cloud security architecture** | Deployed Splunk, Nessus, Palo Alto; managed IRS audit | ✅ STRONG MATCH | Exceptional security architecture experience |
| **SOC 2 audit support** | Maintained SOC 2, FedRAMP, ISO, HIPAA audits | ✅ STRONG MATCH | Direct experience with external auditors |

### 2. Technical Stack Comparison

#### Infrastructure as Code

| Technology | Job Requirement | Candidate Experience | Assessment |
|------------|----------------|---------------------|------------|
| **Terraform** | Required (expert level) | ❌ Not documented | **GAP**: Uses Chef and CloudFormation instead |
| **CloudFormation** | Implied (AWS IaC) | ✅ Used extensively | **MATCH**: Documented AWS CloudFormation experience |
| **Chef** | Not mentioned | ✅ 23 internal cookbooks | **TRANSFERABLE**: Similar declarative IaC concepts |

**Gap Severity:** MODERATE
**Transferability:** HIGH (IaC concepts are transferable; syntax differs)
**Learning Curve:** 2-3 months for proficiency

#### CI/CD Pipeline

| Technology | Job Requirement | Candidate Experience | Assessment |
|------------|----------------|---------------------|------------|
| **GitHub Actions** | Required (CI/CD + security scanning) | ❌ Not documented | **GAP**: Uses Jenkins instead |
| **Jenkins** | Not mentioned | ✅ Forged Jenkins for testing, linting | **MATCH**: Strong CI/CD experience |
| **SAST/DAST scanning** | Required | ⚠️ Security tools (Nessus, BurpSuite) but not in pipeline | **PARTIAL**: Has security scanning, unclear if integrated in CI/CD |

**Gap Severity:** MODERATE
**Transferability:** HIGH (CI/CD concepts are universal)
**Learning Curve:** 1-2 months for GitHub Actions proficiency

#### AWS Services - Serverless Stack

| Service | Job Requirement | Candidate Experience | Assessment |
|---------|----------------|---------------------|------------|
| **Aurora PostgreSQL** | Required (managed database) | ⚠️ PostgreSQL (8 production DBs) | **PARTIAL**: PostgreSQL ops but not Aurora specifically |
| **ECS Fargate** | Required (container orchestration) | ❌ Not documented | **GAP**: No documented container orchestration experience |
| **Lambda** | Required (serverless compute) | ⚠️ EC2, but Lambda not documented | **GAP**: Traditional compute, not serverless |
| **SQS** | Required (messaging) | ❌ Not documented | **GAP**: No documented message queue experience |
| **EC2** | Implied | ✅ Migrated 100+ servers | **MATCH**: Strong EC2 experience |
| **S3** | Implied | ✅ Used extensively | **MATCH**: S3 experience documented |
| **IAM** | Required | ✅ Identity and Access Management | **MATCH**: IAM experience documented |
| **KMS** | Required (secrets/key mgmt) | ❌ Not documented | **GAP**: No documented KMS experience |
| **Secrets Manager** | Required | ❌ Not documented | **GAP**: No documented secrets management tooling |
| **CloudWatch** | Required (observability) | ✅ Used extensively | **MATCH**: Monitoring experience |

**Gap Severity:** HIGH
**Transferability:** MODERATE (AWS ops transfer, but serverless paradigm differs from traditional)
**Learning Curve:** 3-6 months for production-grade serverless architecture

#### Security & Compliance

| Area | Job Requirement | Candidate Experience | Assessment |
|------|----------------|---------------------|------------|
| **SOC 2 audits** | Required | ✅ Maintained SOC 2 with external auditors | **STRONG MATCH**: Direct experience |
| **NIST frameworks** | Implied | ✅ NIST 800-63, NIST 800-53 | **STRONG MATCH**: Multiple NIST frameworks |
| **Vanta platform** | Required | ❌ Not documented | **GAP**: No experience with this compliance automation tool |
| **Security questionnaires** | Required | ⚠️ Not explicitly documented | **UNCLEAR**: Likely did this in compliance role but not documented |
| **Threat modeling** | Preferred | ⚠️ Not documented | **GAP**: No documented threat modeling experience |
| **Vulnerability management** | Required | ✅ Led vuln mgmt, used Nessus, BurpSuite | **STRONG MATCH**: Direct experience |
| **IRS security review** | Not mentioned | ✅ Managed successful IRS on-site review | **ADDITIONAL STRENGTH**: Unique, high-value experience |

**Gap Severity:** LOW
**Transferability:** N/A (already strong in this area)

#### Observability & SRE

| Area | Job Requirement | Candidate Experience | Assessment |
|------|----------------|---------------------|------------|
| **Incident response** | Required | ✅ Led incident response per DHS guidance | **MATCH**: Direct experience |
| **Postmortems** | Implied | ⚠️ Not documented | **GAP**: Common SRE practice but not documented |
| **CloudWatch** | Required | ✅ Used for monitoring | **MATCH**: AWS native monitoring |
| **Prometheus** | Mentioned as equivalent | ❌ Not documented | **GAP**: No documented Prometheus experience |
| **Logging platforms** | Required | ✅ Splunk, Rsyslog | **MATCH**: Logging infrastructure experience |
| **On-call rotation** | Required (escalation partner) | ⚠️ Operations role but not explicit on-call | **UNCLEAR**: Likely did this but not documented |

**Gap Severity:** LOW
**Transferability:** HIGH (SRE practices are universal)

### 3. Leadership & Soft Skills Analysis

| Requirement | Candidate Experience | Assessment |
|-------------|---------------------|------------|
| **Technical leadership** | 4 Director-level roles (DevOps, Security, Compliance, IT) | ✅ STRONG MATCH |
| **Cross-team influence** | Collaborated across dev, ops, security teams | ✅ MATCH |
| **Mentorship** | Mentored 5 junior engineers, coached 4 college hires | ✅ MATCH |
| **Architecture & design reviews** | Validated system designs, reviewed third-party vendors | ✅ MATCH |
| **Escalation & incident handling** | Led incident response, conducted troubleshooting | ✅ MATCH |
| **Communication (technical & non-technical)** | Managed external auditors, vendor contracts, leadership partnership | ✅ STRONG MATCH |

**Gap Severity:** NONE
**Assessment:** Leadership and communication skills are a major strength

### 4. Experience Level Comparison

| Dimension | Job Requirement | Candidate Profile | Gap |
|-----------|----------------|-------------------|-----|
| **Years of experience** | 6+ years | 10+ years (2014-2026) | ✅ EXCEEDS |
| **Seniority level** | Staff Engineer | Director level (4 director roles) | ✅ EXCEEDS |
| **Team size influenced** | Multiple teams | Led teams, mentored engineers, influenced org-wide standards | ✅ MATCHES |
| **Scale of systems** | Production systems | 10M+ daily users, 100+ server infrastructure | ✅ MATCHES |
| **Compliance scope** | SOC 2, audit support | SOC 2, FedRAMP, ISO, HIPAA, IRS full-scope | ✅ EXCEEDS |

**Overall:** Candidate is overqualified in terms of seniority and breadth, but gaps exist in specific modern tooling.

---

## Gap Categories

### Category 1: Critical Gaps (Must Address)

**Definition:** Technologies explicitly required that candidate lacks direct experience with.

| Gap | Severity | Impact on Job Performance | Mitigation Strategy |
|-----|----------|--------------------------|---------------------|
| **Terraform** | HIGH | Central to role (IaC standards ownership) | ⚠️ BLOCKER: Need to demonstrate IaC transfer, fast learning, or get basic Terraform experience pre-interview |
| **Serverless stack (ECS Fargate, Lambda, SQS)** | HIGH | Core AWS architecture for company | ⚠️ MAJOR: Company is serverless-first; traditional EC2 experience may not transfer enough |
| **Vanta compliance platform** | MEDIUM | Required tool for compliance automation | ⚠️ MODERATE: Can learn on the job, but shows lack of modern compliance tooling |

**Recommendation:** These gaps may be disqualifiers without strong narrative around transferable skills and rapid learning ability.

### Category 2: Transferable Gaps (Addressable)

**Definition:** Candidate has adjacent experience that could transfer with moderate effort.

| Gap | Transferable Experience | Transfer Difficulty | Strategy |
|-----|------------------------|--------------------|-----------|
| **Terraform** | Chef + CloudFormation (IaC concepts) | MODERATE | Emphasize IaC expertise; show Terraform learning in progress |
| **GitHub Actions** | Jenkins CI/CD | LOW | Highlight CI/CD architecture skills; mention YAML-based pipeline experience |
| **Aurora PostgreSQL** | 8 production PostgreSQL databases | LOW | Emphasize PostgreSQL expertise; Aurora is managed version |
| **Multi-account AWS** | AWS infrastructure management | MODERATE | Discuss governance, isolation, IAM strategy from current work |

**Recommendation:** Frame these as "tool differences, not skill gaps" in interview conversations.

### Category 3: Minor Gaps (Low Impact)

**Definition:** Skills that are nice-to-have or can be quickly learned on the job.

| Gap | Learning Curve | Priority |
|-----|---------------|----------|
| **Prometheus** | 1-2 weeks | LOW (has Splunk, CloudWatch) |
| **KMS / Secrets Manager** | 1-2 weeks | LOW (has secrets mgmt concepts) |
| **Postmortem facilitation** | 1 week | LOW (has incident response experience) |
| **Cost optimization** | 2-4 weeks | LOW (has infrastructure ops, will learn patterns) |

**Recommendation:** Don't emphasize these gaps; they're easily learned on the job.

---

## Strengths Analysis

### Unique Differentiators

**These are strengths the candidate has that many Staff DevSecOps Engineers lack:**

1. **Government/High-Security Environment Experience**
   - IRS on-site full-scope security review (successful)
   - FedRAMP compliance (NIST 800-53)
   - Identity verification for National Strategy for Trusted Identities in Cyberspace (NSTIC)
   - **Value:** Demonstrates ability to operate under extreme scrutiny and regulatory pressure

2. **Multi-Framework Compliance Expertise**
   - SOC 2, FedRAMP, ISO, HIPAA simultaneously
   - External auditor relationships (Kantara, FedRAMP auditors)
   - **Value:** Most DevSecOps engineers have 1-2 frameworks; candidate has 4+ with audit success

3. **Dual Security & Operations Leadership**
   - Both Director of Security AND Director of DevOps
   - Rare combination of offensive security mindset with operational reliability focus
   - **Value:** Understands both "break it" and "keep it running" perspectives

4. **Scale Experience**
   - 10M+ daily active users
   - 100+ server migration
   - 8 production PostgreSQL databases
   - **Value:** Proven ability to operate at scale, not just small startups

### Competitive Advantages

**Why this candidate might be preferred over others:**

| Advantage | Why It Matters for LODAS |
|-----------|--------------------------|
| **Compliance-first mindset** | LODAS is in financial services (alternative investments) = heavily regulated; candidate's compliance DNA is rare and valuable |
| **Security questionnaire experience** | Job explicitly mentions handling security questionnaires; candidate likely did this extensively in compliance director role |
| **Audit readiness** | "Continuous control monitoring and audit readiness" is in job description; candidate has maintained 4+ simultaneous audit frameworks |
| **Operational excellence at scale** | 99.99% uptime, 10M+ users shows reliability focus, which job emphasizes ("highest standards of reliability") |
| **Leadership without ego** | Multiple director roles show proven leadership, but applying for Staff Engineer role shows focus on technical work over titles |

---

## Risk Assessment

### Risks of Hiring This Candidate

| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| **Steep learning curve for Terraform** | MEDIUM | MEDIUM | Pair with Terraform expert for 1st month; candidate's IaC background suggests fast ramp |
| **Serverless paradigm shift** | MEDIUM | HIGH | Assign serverless projects early; provide training; candidate's AWS depth should help |
| **Overqualified (director → staff)** | LOW | LOW | Candidate is choosing technical work over management; likely stable |
| **Modern tooling gap (Terraform, GitHub Actions)** | HIGH | MEDIUM | Cultural fit question: does company prefer "grow with modern tools" or "battle-tested with legacy"? |

### Risks of NOT Hiring This Candidate

| Risk | Impact |
|------|--------|
| **Miss rare security + compliance + DevOps combination** | HIGH: This skillset combination is extremely rare in market |
| **Lose candidate with proven audit success** | MEDIUM: Compliance is critical for financial services; candidate has track record |
| **Alternative candidates may lack depth** | MEDIUM: Typical Staff DevSecOps engineer may have modern tools but lack security/compliance depth |

---

## Interview Focus Areas

### Questions to Validate Gaps

**Terraform & IaC:**
1. "You've used Chef and CloudFormation extensively. Walk me through how you'd approach learning Terraform if hired. What IaC concepts transfer?"
2. "Describe a complex infrastructure problem you solved with IaC. How would you approach it differently with Terraform vs. Chef?"

**Serverless Architecture:**
1. "Our stack is serverless-first (ECS Fargate, Lambda, SQS). You have strong EC2/traditional compute experience. How do you think about the serverless paradigm differently?"
2. "Have you worked with event-driven architectures or message queues? How would you design a serverless system?"

**Modern CI/CD:**
1. "You've built CI/CD with Jenkins. GitHub Actions is YAML-based and event-driven. How quickly do you typically pick up new CI/CD platforms?"
2. "Describe how you'd integrate SAST/DAST scanning into a GitHub Actions pipeline you're building from scratch."

**Security Leadership:**
1. "You've managed IRS audits and SOC 2 simultaneously. Walk us through how you'd approach owning Vanta and compliance automation here."
2. "How do you balance 'security by design' with 'move fast and iterate' in a startup environment?"

### Questions to Validate Strengths

**Compliance & Audit:**
1. "Tell me about the most complex compliance challenge you've faced. How did you navigate it?"
2. "How do you prepare engineering teams for security audits without creating friction?"

**Incident Response:**
1. "Describe your most memorable production incident. What was your role, and what systemic improvements resulted?"
2. "How do you handle being an escalation partner without becoming a bottleneck?"

**Leadership & Influence:**
1. "You've been a director but are applying for a staff role. What drives this decision?"
2. "How do you influence technical decisions across teams when you're not the manager?"

---

## Recommendations

### For the Candidate (Tom)

**Short-term Actions (Before Applying):**

1. **Address Terraform Gap:**
   - [ ] Complete "Terraform: Up and Running" or HashiCorp tutorials (20 hours)
   - [ ] Build a sample project: "Multi-account AWS setup with Terraform" to demonstrate learning
   - [ ] Add to resume: "Currently deepening Terraform expertise (provisioned X resources in Y project)"

2. **Demonstrate Serverless Learning:**
   - [ ] Complete AWS Lambda + SQS tutorial (10 hours)
   - [ ] Build a small event-driven project: API Gateway → Lambda → SQS → Lambda → Aurora
   - [ ] Add to resume: "Exploring serverless patterns (built X event-driven system)"

3. **Update Resume Immediately:**
   - [ ] Add "GitHub Actions" if you've used it at all (even personal projects)
   - [ ] Change "PostgreSQL" to "Aurora PostgreSQL" if you're comfortable with the equivalence
   - [ ] Add "Vanta" if you've evaluated it or used similar compliance automation
   - [ ] Emphasize "Infrastructure as Code" in summary (not just "Chef")
   - [ ] Add "Multi-account AWS strategy" if you've designed account structure

4. **Prepare Strong Narratives:**
   - [ ] "Why I'm moving from Director to Staff": Focus on technical depth over management
   - [ ] "IaC tool transfer": Chef → Terraform is syntax, not concepts
   - [ ] "Unique value": Security + Compliance + DevOps is rare; tools can be learned

**Long-term Actions (During Interview Process):**

1. **Showcase Learning Velocity:**
   - Build a small Terraform + GitHub Actions project during interview process
   - Share GitHub repo demonstrating rapid skill acquisition

2. **Lean Into Compliance Differentiator:**
   - Prepare case study: "How I maintained SOC 2 + FedRAMP + ISO + HIPAA simultaneously"
   - Emphasize financial services readiness

3. **Address Gaps Proactively:**
   - Don't wait for them to ask; address Terraform/serverless gaps upfront
   - Frame as "excited to dive deeper into modern serverless stack"

### For the Hiring Manager (LODAS)

**Decision Framework:**

**Hire if:**
- ✅ Compliance and security depth is critical (financial services = yes)
- ✅ You value proven audit success over modern tooling
- ✅ You're willing to invest 3-6 months in serverless + Terraform training
- ✅ You need someone who can handle security questionnaires and audits immediately

**Don't hire if:**
- ❌ You need someone productive in Terraform + serverless on day 1
- ❌ You can't afford 3-6 month ramp time for modern stack
- ❌ Cultural fit prefers "grew up with modern tools" over "battle-tested veteran"

**Interview Plan:**

1. **Technical Screen (2 hours):**
   - IaC concepts (tool-agnostic)
   - AWS architecture (serverless scenario)
   - Security + compliance scenarios

2. **Onsite Interviews:**
   - Architecture: Design a multi-account AWS serverless system
   - Security: Incident response simulation
   - Leadership: Cross-team influence scenario
   - Cultural Fit: Why staff role after director roles?

3. **Take-home (Optional):**
   - "Build a Terraform module for X" → Tests learning ability
   - "Design CI/CD pipeline with security scanning" → Tests transferability

---

## Conclusion

**Overall Recommendation:** CONSIDER WITH CAVEATS

**Summary:**

Tom Robison is a **rare security + compliance + DevOps hybrid** with exceptional depth in audit frameworks (SOC 2, FedRAMP, NIST), proven ability to operate at scale (10M+ users), and successful high-stakes security reviews (IRS). His leadership experience (4 director roles) exceeds the staff level, but he's deliberately seeking technical depth over management.

**The trade-off is clear:**
- ✅ **You get:** Exceptional security/compliance depth, proven audit success, leadership maturity, operational excellence at scale
- ❌ **You give up:** Day-1 productivity in Terraform/GitHub Actions/serverless stack; 3-6 month ramp time needed

**For a financial services company (LODAS) in a regulated space, this trade-off likely favors hiring** — the compliance expertise is rare and directly applicable, while the modern tooling gap is addressable through training and mentorship.

**Key success factors if hired:**
1. Pair with Terraform expert for first 2 months
2. Assign serverless project early (Lambda + SQS + ECS Fargate)
3. Leverage compliance expertise immediately (Vanta, SOC 2, security questionnaires)
4. Use as security SME while ramping technical stack

**Alternative framing:** You're hiring a **proven security + compliance leader** who happens to need 3-6 months to learn your specific tooling — not the other way around.

---

## Appendix: Data Summary

### Keyword Match Breakdown

**Matched Required Keywords (9/29 = 31.0%):**
- AWS
- infrastructure as code
- CI/CD
- security
- compliance
- Lambda
- IAM
- SOC 2
- CloudWatch

**Missed Required Keywords (20/29 = 69.0%):**
- Terraform
- GitHub Actions
- Aurora
- ECS Fargate
- SQS
- serverless
- KMS
- Secrets Manager
- Vanta
- SAST
- DAST
- vulnerability
- observability
- monitoring
- incident response
- reliability
- SRE
- mentorship
- technical leadership
- architecture

**Matched Preferred Keywords (5/9 = 55.6%):**
- PostgreSQL
- automation
- Python
- NIST
- postmortem

**Missed Preferred Keywords (4/9 = 44.4%):**
- multi-account
- threat modeling
- encryption
- cost optimization

### Experience File Analysis

**Files Analyzed:**
1. `idme-director-security.md` (5 achievements, 41 keywords)
2. `idme-director-devops.md` (7 achievements, 46 keywords)
3. `idme-director-compliance.md` (4 achievements, 35 keywords)
4. `idme-director-it.md` (5 achievements, 28 keywords)

**Total Resume Content:**
- 21 achievements across 4 roles
- 150+ unique keywords
- 10+ years documented experience (2014-2026)
- 4 director-level roles

**Resume Generation Metadata:**
- Generated: 2026-02-13
- Target length: 2 pages
- Actual length: 0.7 pages (under target)
- Optimization strategy: keyword-dense
- Config version: security-lead

---

**Document Version:** 1.0
**Generated by:** Resume Tailoring System Gap Analysis Module
**For use with:** explore-candidate skill (in development)
