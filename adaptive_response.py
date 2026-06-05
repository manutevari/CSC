import re

from core_knowledge_pack import CORE_SERVICE_KEYWORDS, CORE_SERVICE_PROFILE_CONTEXTS


MODE_SECTIONS = {
    "overview": {
        "who_can_use",
        "eligibility",
        "important_notes",
        "faq",
        "official_links",
    },
    "dsp_training": {
        "who_can_use",
        "prerequisites",
        "dsp_navigation",
        "workflow",
        "status_tracking",
        "approval_process",
        "download_print",
        "common_errors",
        "important_notes",
        "faq",
        "official_links",
    },
    "form_filling": {
        "who_can_use",
        "eligibility",
        "prerequisites",
        "documents",
        "form_filling",
        "validation_rules",
        "upload_requirements",
        "workflow",
        "status_tracking",
        "approval_process",
        "download_print",
        "common_errors",
        "important_notes",
        "faq",
        "official_links",
    },
    "troubleshooting": {
        "prerequisites",
        "status_tracking",
        "common_errors",
        "important_notes",
        "faq",
        "official_links",
    },
    "documentation": {
        "who_can_use",
        "eligibility",
        "prerequisites",
        "documents",
        "fee_information",
        "upload_requirements",
        "important_notes",
        "faq",
        "official_links",
    },
    "circular": {
        "policies_circulars",
        "fee_information",
        "important_notes",
        "faq",
        "official_links",
    },
    "comparison": {
        "who_can_use",
        "documents",
        "comparison",
        "workflow",
        "important_notes",
        "faq",
        "official_links",
    },
    "catalog": {
        "who_can_use",
        "prerequisites",
        "dsp_navigation",
        "form_filling",
        "workflow",
        "status_tracking",
        "approval_process",
        "download_print",
        "common_errors",
        "important_notes",
        "faq",
        "official_links",
    },
}


RESPONSE_MODE_KEYWORDS = (
    ("catalog", ("all csc", "all services", "all forms", "service list", "catalog", "categories", "सभी सेवा", "सभी फॉर्म")),
    ("circular", ("latest", "circular", "policy change", "fee update", "suspension", "notice", "announcement", "सर्कुलर", "नीति", "अपडेट")),
    ("comparison", ("compare", "difference", " vs ", "versus", "reprint vs correction", "correction vs reprint", "अंतर", "तुलना")),
    ("troubleshooting", ("error", "issue", "problem", "not working", "failed", "pending", "rejected", "device not detected", "settlement", "troubleshoot", "समस्या", "एरर", "फेल")),
    ("documentation", ("documents", "document", "docs", "fees", "fee", "eligibility", "required", "charges", "दस्तावेज", "फीस", "योग्यता")),
    ("form_filling", ("fill", "form", "application", "field", "upload", "apply", "registration", "register", "enroll", "enrol", "enrollment", "enrolment", "claim", "correction", "update", "reprint", "duplicate", "lost", "book", "booking", "फॉर्म", "भर", "आवेदन", "रजिस्ट्रेशन", "सुधार")),
    ("dsp_training", ("how to", "how to use", "how to become", "use", "navigation", "menu", "click", "login", "digital seva", "dsp", "portal", "status", "track", "tracking", "download", "print", "approval", "process", "workflow", "steps", "cash withdrawal", "balance enquiry", "mini statement", "biometric process", "consultation", "appointment", "certificate", "course", "cancellation", "कैसे", "कैसे उपयोग", "लॉगिन", "मेन्यू", "स्टेटस", "स्थिति", "प्रक्रिया")),
    ("overview", ("what is", "about", "purpose", "explain", "क्या है", "बताओ")),
)


SERVICE_PROFILE_CONTEXTS = {
    "digipay": """Source: https://digipay.csccloud.in/
Service/form: DigiPay
Purpose:
DigiPay is a CSC banking/financial service used by authorized VLEs for Aadhaar-enabled and related digital transactions through the official DigiPay application/portal.
Who Can Use:
Authorized CSC/VLE or banking correspondent role where DigiPay is enabled.
Prerequisites:
- Active CSC/VLE credentials with DigiPay access.
- DigiPay application/portal access.
- Internet connectivity.
- Registered biometric/iris/Micro ATM device and RD/device service where required.
- Printer or receipt method if the transaction receipt has to be given.
DSP Navigation:
1. Login to Digital Seva Portal or open the official DigiPay application/portal if enabled for the VLE.
2. Select the required DigiPay transaction/service.
3. Confirm device/RD service status before starting biometric or Micro ATM flow.
4. Continue only on the official DigiPay screen.
Form Filling Guide:
1. Select transaction type such as cash withdrawal, balance enquiry, mini statement, DMT, bill payment, wallet, or Micro ATM only if shown in DigiPay.
2. Enter customer details only on the DigiPay screen.
3. Enter amount/bank/service details carefully.
4. Capture biometric/OTP/device authentication only on the official screen.
5. Confirm success/failure status and give receipt.
Common Validation Rules:
- Customer consent is required before transaction.
- Aadhaar, bank, OTP, biometric, or transaction data must not be entered in chat.
- Amount and bank/service selection must match the customer request.
Upload Requirements:
- Upload is normally not part of a simple transaction unless DigiPay asks for KYC/device/agent documents.
Application Workflow:
1. Check device and login.
2. Select transaction/service.
3. Enter required customer/transaction details.
4. Complete biometric/OTP/device authentication.
5. Submit transaction.
6. Save/print receipt and check passbook/transaction status.
Status Tracking:
Use DigiPay transaction history, passbook, receipt number, or official support/status option shown inside DigiPay.
Approval Process:
Agent onboarding, device registration, settlement, or blocked transaction review depends on DigiPay/CSC/bank workflow.
Download / Print:
Print or save transaction receipt/passbook entry from DigiPay if the option is available.
Common Errors:
- Biometric device not detected. Cause: device/RD service not ready. Resolution: reconnect device, check RD service, and retry on official screen.
- Biometric authentication failed. Cause: poor capture or mismatch. Resolution: clean sensor/finger and retry only with customer consent.
- Transaction pending. Cause: bank/network response pending. Resolution: check transaction status/passbook before repeating.
- Payment/settlement issue. Cause: reconciliation or bank response. Resolution: use official DigiPay status/support flow.
- Wrong amount/bank selected. Cause: data entry mistake. Resolution: review details before biometric submit.
Important Notes:
- Always give receipt for transaction success/failure where DigiPay provides it.
- Never store or share customer Aadhaar, bank, OTP, or biometric data outside the official DigiPay flow.
Official URL:
https://digipay.csccloud.in/""",
    "ayushman": """Source: https://beneficiary.nha.gov.in/
Source: https://www.pmjay.gov.in/
Service/form: Ayushman Bharat / PM-JAY
Purpose:
Ayushman Bharat PM-JAY service helps eligible beneficiaries search/verify family details and generate/download health card where the official NHA/PM-JAY flow allows it.
Who Can Use:
Eligible beneficiary/family and authorized CSC/VLE or official role where PM-JAY/Ayushman service is enabled.
Eligibility:
Eligibility must be confirmed only through the official PM-JAY/NHA beneficiary search or official scheme data.
Prerequisites:
- Citizen consent.
- Beneficiary/family search details as required by official portal.
- eKYC method such as OTP/biometric only if asked by the official portal.
- Active mobile/ID/document details only inside official portal fields.
DSP Navigation:
1. Login to DSP if Ayushman/PM-JAY service is enabled, or open the official NHA/PM-JAY beneficiary portal.
2. Select beneficiary search/card/eKYC service shown by the portal.
3. Search beneficiary/family as per official fields.
4. Continue eKYC and card flow only on the official portal.
Form Filling Guide:
1. Select state/scheme/search option shown by the portal.
2. Enter beneficiary/family search details only in official fields.
3. Verify family/member details shown by the portal.
4. Complete eKYC/OTP/biometric only if the portal requires it.
5. Submit and save beneficiary/card/reference status.
Common Validation Rules:
- Do not create eligibility manually.
- Name, age, family, mobile, and ID details must match official records.
- OTP/biometric must be used only with beneficiary consent.
Upload Requirements:
- Upload documents only if the official NHA/PM-JAY portal asks.
Application Workflow:
1. Search beneficiary.
2. Verify family/member details.
3. Complete eKYC if required.
4. Submit verification/card request.
5. Download/print card if generated.
Status Tracking:
Use the official beneficiary/card status shown on the NHA/PM-JAY portal.
Approval Process:
Approval or card generation depends on official PM-JAY/NHA workflow and eligibility data.
Download / Print:
Download/print Ayushman card only after the official portal generates it.
Common Errors:
- Beneficiary not found. Cause: search details do not match official data. Resolution: retry with correct official details.
- eKYC failed. Cause: OTP/biometric mismatch or network issue. Resolution: retry only through official portal with consent.
- Family details mismatch. Cause: record mismatch. Resolution: follow official correction/helpdesk flow.
- Card not generated. Cause: eligibility/eKYC/approval pending. Resolution: check official status.
Official URL:
https://beneficiary.nha.gov.in/
Official Helpdesk:
Use help/contact options shown on the official PM-JAY/NHA portal.
Official Tracking Page:
https://beneficiary.nha.gov.in/""",
    "fssai": """Source: https://foscos.fssai.gov.in/
Source: https://foscos.fssai.gov.in/public/fbo/view-NOC-application-reg
Service/form: FSSAI FoSCoS License / Registration
Purpose:
FoSCoS is the official FSSAI portal for food business license/registration, renewal, modification, annual return, and application tracking.
Who Can Use:
Food Business Operator or authorized representative using the official FoSCoS flow.
Eligibility:
Eligibility depends on food business type, state, kind of business, and official FSSAI rules shown on FoSCoS.
Prerequisites:
- Food business details.
- Kind of Business selection.
- Premises/address details.
- PAN and required business/person documents where official FoSCoS asks.
- Payment method for official FoSCoS fee if applicable.
Required Documents:
- Documents required depend on new license, renewal, modification, registration, and Kind of Business.
- Use the FoSCoS Documents Required section for exact document list.
DSP Navigation:
1. Login to DSP only if FSSAI service is enabled, or open FoSCoS directly.
2. Select New License/Registration, Renew, Modify, Annual Return, or Track Application as required.
3. Select state, business type, and Kind of Business as shown by FoSCoS.
4. Continue only on official FoSCoS pages.
Form Filling Guide:
1. Select the correct application type.
2. Fill FBO/business name, address, contact, premises, and Kind of Business details.
3. Enter PAN and other identifiers only in official FoSCoS fields.
4. Upload documents required for the selected license/registration type.
5. Pay official fee only through FoSCoS.
Common Validation Rules:
- Kind of Business must match the actual food business.
- PAN/business details must match documents.
- Captcha and mandatory fields must be completed.
Upload Requirements:
- Upload self-attested documents where official FoSCoS requires it.
- Use clear files in the allowed format/size shown by FoSCoS.
Application Workflow:
1. Select application type.
2. Fill business/FBO details.
3. Upload required documents.
4. Pay fee on FoSCoS.
5. Submit and save application/reference number.
Status Tracking:
Use the Track Application option on FoSCoS.
Approval Process:
Approval/inspection depends on FSSAI/State authority workflow and application type.
Download / Print:
Download/print license, registration certificate, acknowledgement, or application copy from FoSCoS when available.
Common Errors:
- Wrong Kind of Business. Cause: incorrect category selection. Resolution: verify KoB before submit.
- Missing document. Cause: required document not uploaded. Resolution: use Documents Required section.
- Payment warning/fraud risk. Cause: non-official payment link. Resolution: pay only through FoSCoS.
- Captcha/session issue. Cause: session expired or captcha mismatch. Resolution: refresh official page and retry.
Important Notes:
- Official FoSCoS page warns that payments for License/Registration should be made only through https://foscos.fssai.gov.in.
- FoSCoS announcements may affect documents, PAN compliance, fees, or process. Use indexed/live official circular text for latest circular answers.
- Official FoSCoS helpdesk shown on the portal: helpdesk-foscos@fssai.gov.in and 1800-11-2100.
Official URL:
https://foscos.fssai.gov.in/
Official Helpdesk:
helpdesk-foscos@fssai.gov.in
Official Tracking Page:
https://foscos.fssai.gov.in/""",
    "passport": """Source: https://www.passportindia.gov.in/psp/GettingStarted
Source: https://portal2.passportindia.gov.in/AppOnlineProject/statusTracker/trackStatusForFileNoNew
Service/form: Passport Seva
Purpose:
Passport Seva is the official Ministry of External Affairs portal for passport application, appointment, fee payment, status tracking, and related services.
Who Can Use:
Indian citizen/applicant or authorized assistance role using the official Passport Seva portal.
Eligibility:
Eligibility and service type depend on Passport Seva rules, applicant category, fresh/reissue case, and documents.
Prerequisites:
- Passport Seva account/login where required.
- Correct service type such as fresh, reissue, Tatkaal, minor, or other service.
- Required supporting documents and fee payment.
Required Documents:
- Proof of date of birth.
- Identity proof with photograph.
- Proof of residence.
- Proof of nationality as verified by Passport Seva officials.
DSP Navigation:
1. Login to DSP only if Passport service is enabled, or open the official Passport Seva portal.
2. Use New User Registration/Existing User Login if needed.
3. Select the correct passport service and application flow.
4. Book appointment and visit PSK/POPSK/RPO as instructed.
Form Filling Guide:
1. Select fresh/reissue/service type correctly.
2. Fill applicant name, date of birth, address, contact, family, and identity details as per documents.
3. Pay fee and schedule appointment only on official Passport Seva portal.
4. Carry original documents to PSK/POPSK/RPO appointment.
Common Validation Rules:
- Mandatory status tracking fields include application type, file number, and date of birth.
- Details must match documents.
Upload Requirements:
- Upload or carry documents only as instructed by Passport Seva.
Application Workflow:
1. Register/login.
2. Fill application.
3. Pay fee/schedule appointment.
4. Visit PSK/POPSK/RPO with original documents.
5. Police verification/processing happens as applicable.
Status Tracking:
Track application with application type, file number, and date of birth on the official Passport Seva tracking page.
Approval Process:
Passport issue depends on document verification, prescribed procedure, PSK/RPO processing, and police verification where applicable.
Download / Print:
Use Print Application Form or appointment/receipt options on Passport Seva when available.
Common Errors:
- Fake website/payment risk. Cause: unofficial portal. Resolution: use only www.passportindia.gov.in.
- Required document missing. Cause: incomplete supporting documents. Resolution: carry prescribed documents to appointment.
- Invalid file number/status input. Cause: wrong tracking details. Resolution: enter correct file number and date of birth.
Important Notes:
- Passport Seva warns against fraudulent websites and states that the official site is www.passportindia.gov.in.
Official URL:
https://www.passportindia.gov.in/
Official Tracking Page:
https://portal2.passportindia.gov.in/AppOnlineProject/statusTracker/trackStatusForFileNoNew""",
    "gst": """Source: https://www.gst.gov.in/
Source: https://services.gst.gov.in/services/login
Service/form: GST Portal Services
Purpose:
The GST portal is used for GST registration, returns, payments, refunds, ledgers, user services, and taxpayer services.
Who Can Use:
Taxpayer, business, authorized representative, or facilitation role using official GST portal credentials.
Eligibility:
Eligibility depends on GST law, business activity, turnover, registration type, and official GST rules.
Prerequisites:
- Correct taxpayer/business details.
- PAN, mobile/email, address, bank/business documents if official GST service asks.
- GST portal login/credentials where required.
DSP Navigation:
1. Login to DSP only if GST service is enabled, or open the official GST portal.
2. Use GST portal Services menu.
3. Select Registration, Returns, Payments, Refunds, Ledgers, or User Services as required.
4. Continue only on official GST portal pages.
Form Filling Guide:
1. Select the exact GST service.
2. Enter taxpayer/business details only on official GST portal fields.
3. Upload required documents if the selected GST service asks.
4. Verify, submit, and save ARN/reference/acknowledgement.
Common Validation Rules:
- PAN/GSTIN/details must match official records.
- Mandatory fields and captcha/OTP must be completed only on official portal.
- Return/payment period must be selected correctly.
Application Workflow:
1. Select GST service.
2. Fill details.
3. Validate/verify.
4. Submit and save ARN/reference.
5. Track status or download certificate/acknowledgement where available.
Status Tracking:
Use the GST portal status/ARN/service page for tracking.
Download / Print:
Use GST portal download/view certificate or acknowledgement option where available.
Common Errors:
- Wrong service/period selected. Cause: incorrect menu or tax period. Resolution: verify before submit.
- OTP/captcha failed. Cause: mismatch/session. Resolution: retry on official portal.
- ARN/status pending. Cause: processing pending. Resolution: track on GST portal.
Official URL:
https://www.gst.gov.in/
Official Tracking Page:
https://www.gst.gov.in/""",
}


SERVICE_KEYWORDS = (
    ("digipay", ("digipay", "digi pay", "aeps", "micro atm", "matm", "cash withdrawal", "rd service", "biometric device", "डिजीपे", "डिजी पे", "बायोमेट्रिक डिवाइस")),
    ("ayushman", ("ayushman", "pmjay", "pm-jay", "abha", "beneficiary nha", "ayushman card", "आयुष्मान", "पीएमजय", "पीएम-जय", "आयुष्मान कार्ड")),
    ("fssai", ("fssai", "foscos", "food license", "food registration", "food business", "एफएसएसएआई", "फॉस्कोस", "फूड लाइसेंस")),
    ("passport", ("passport", "passport seva", "psk", "popsk", "पासपोर्ट")),
    ("gst", ("gst", "gstin", "goods and services tax", "जीएसटी")),
)


SERVICE_PROFILE_CONTEXTS = {**CORE_SERVICE_PROFILE_CONTEXTS, **SERVICE_PROFILE_CONTEXTS}
SERVICE_KEYWORDS = CORE_SERVICE_KEYWORDS + SERVICE_KEYWORDS


def detect_response_mode(query):

    text = f" {(query or '').lower()} "
    for mode, terms in RESPONSE_MODE_KEYWORDS:
        if any(_term_matches(text, term) for term in terms):
            return mode

    return "overview"


def sections_for_mode(mode):

    return MODE_SECTIONS.get(mode, MODE_SECTIONS["overview"])


def profile_context(query, language="en"):

    if detect_response_mode(query) == "catalog":
        return ""

    service = detect_service_key(query)
    if not service:
        return ""

    return SERVICE_PROFILE_CONTEXTS.get(service, "")


def detect_service_key(query):

    text = f" {(query or '').lower()} "
    for service, terms in SERVICE_KEYWORDS:
        if any(_term_matches(text, term) for term in terms):
            return service

    return ""


def _term_matches(text, term):

    if any(ord(char) > 127 for char in term):
        return term in text

    pattern = r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])"
    return bool(re.search(pattern, text))
