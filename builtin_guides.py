import re

from adaptive_response import profile_context


PAN_GUIDE_CONTEXT = """Source: https://www.incometax.gov.in/iec/foportal/help/all-topics/instant-e-pan/faq
Source: https://www.protean-tinpan.com/services/pan/pan-index.html
Source: https://www.pan.utiitsl.com/PAN/
Service/form: PAN card application / PAN correction through official PAN service portals used for PAN services.

CSC form-filling guide for PAN card:
1. Select the correct PAN service: new PAN, correction/change in PAN data, reprint/reissue, or e-PAN if available on the official portal.
2. Select the applicant category carefully: individual, firm, company, trust, HUF, or other category shown by the portal.
3. For Indian citizens/entities, PAN applications generally use Form 49A. For foreign citizens/entities, PAN applications generally use Form 49AA. For correction, use the correction/change request option.
4. Fill name exactly as per proof documents. Keep surname, first name, and middle name consistent with the applicant document.
5. Fill father's name/mother's name, date of birth or incorporation, gender, and contact details only as required by the official portal.
6. Fill address details from valid proof. Check PIN code, state, district, and communication address carefully.
7. Enter Aadhaar/PAN/mobile/email only inside the official PAN portal if required. Do not paste Aadhaar, PAN, OTP, or document numbers into this chatbot.
8. Upload or submit proof of identity, proof of address, and proof of date of birth as required by the selected applicant category and mode.
9. Check photo, signature, declaration, consent, payment, and acknowledgement before final submission.
10. After submission, save the acknowledgement number/receipt from the official portal and track status only on the official PAN/service portal.

DPDP note: CSC/VLE should collect only the data required by the official PAN portal, show consent/declaration clearly, avoid storing unnecessary copies, and never share Aadhaar/PAN/OTP in chat."""


DIGITAL_SEVA_SERVICES_CONTEXT = """Source: https://digitalseva.csc.gov.in/web/services
Service/form group: Digital Seva Portal services.

Official Digital Seva Portal service categories and example services:
- Aadhaar: Aadhaar Demographic Update, Aadhaar Mobile Update, Best Finger Detection, Aadhaar eKYC PVC Print.
- Agriculture: Agricultural Machine Store, Online Store, Farmer Registration, Marketplace.
- Banking and Pension: RAP Registration, Basic Banking Course, Life Certificate (LIC), Pin Pad Device Payment Service.
- Education: SCLM Registration, SCLM Admission, Tally Certification, eLegal Consultancy.
- Election: Punjab Election Services, Uttarakhand Election Services, Meghalaya Election Services, Rajasthan Election Services.
- Electricity: Online Bill Payment (Non-RAPDRP), Online Bill Payment (RAPDRP), Online Bill Payment.
- Government: Birth and Death Application, Forest Services, Online FIR, Ration Card Services.
- Health: Super Speciality Consultation, Telemedicine, Jan Aushadhi Registration, Jiva Telemedicine.
- Insurance: Pradhan Mantri Fasal Bima Yojna, Farmer Package Policy, Life Insurance, Personal Accidental.
- Skills: CAD Registration, Self Animation Course, Digital Unnati, Training Courses.
- Travel: Darshan Booking, Bus Ticket Booking, Flight Tickets, Bus Tickets.
- Others: PVC Card and Biometric Device, Pradhan Mantri Awas Yojana, Jeevan Pramaan, NIELIT Facilitation Centre.

Class 8 level guide to fill any Digital Seva service form:
1. First read the service name carefully. Choose only the service the citizen actually needs.
2. Open the Digital Seva Portal or the official service page shown by CSC.
3. Login only with the VLE/authorized account. Do not share password or OTP with anyone.
4. Before typing, keep the required documents ready. The exact documents depend on the service.
5. Take clear consent from the citizen before entering their details.
6. Fill basic details slowly: name, date, address, mobile, category, location, and other fields exactly as shown in the citizen's documents.
7. If the form asks for an ID number, enter it only inside the official portal. Do not type Aadhaar, PAN, bank details, OTP, or document numbers in this chatbot.
8. Upload only the documents asked by the official portal. Check file size, photo clarity, and correct document type.
9. Recheck spelling, numbers, district, state, dates, and uploaded files before submission.
10. Complete payment only on the official portal if the service requires payment.
11. Save or print the acknowledgement, receipt, application number, or reference number.
12. Tell the citizen how to track the application status on the official portal/helpdesk.

Important limitation: The Digital Seva services page lists services and categories, but exact field names, fee, eligibility, and document list can be different for each service. If a field/document is not visible in the indexed official source text, verify it inside the official Digital Seva/service portal before submission.

DPDP note: Collect only the information needed for that service, explain consent, keep documents safe, and do not store or share unnecessary personal data."""


TAX2WIN_GUIDE_CONTEXT = """Source: https://tax2win.in/
Source: https://www.incometax.gov.in/
Service/form: Tax2Win / Income Tax Return filing guidance for citizens using an official tax filing service.

Class 8 level guide to fill an ITR/Tax2Win form:
1. First confirm the service: income tax return filing, tax calculation, refund tracking, or tax notice/help.
2. Ask the citizen to keep documents ready before starting: PAN, Aadhaar as required by the official portal, Form 16, salary slips, bank details, interest certificates, rent/loan details, investment proofs, AIS/TIS, Form 26AS, and deduction proofs if applicable.
3. Do not collect or type PAN, Aadhaar, bank account number, password, or OTP in this chatbot. Enter such details only inside the official Tax2Win/Income Tax portal.
4. Select the correct financial year/assessment year.
5. Select the correct ITR type only as guided by the official portal or tax expert. If unsure, verify before filing.
6. Fill personal details carefully: name, date of birth, PAN, address, email, mobile, and bank details exactly as shown in official records.
7. Fill income details from Form 16, salary slips, interest certificates, business/profession records, capital gains records, or other official documents.
8. Fill deductions/exemptions only when the citizen has proof. Do not add fake deductions.
9. Check tax paid/TDS from Form 26AS/AIS/TIS and match it with the return.
10. Review refund/payable amount, declaration, consent, and final summary before submission.
11. Submit only after the citizen confirms all details are correct.
12. Complete e-verification on the official portal if required.
13. Save acknowledgement/ITR-V/reference number and tell the citizen how to track status.

Important limitation: Tax filing rules depend on income type, year, documents, and law updates. If exact field names, ITR type, tax amount, or eligibility is not visible in official source data, verify inside the official portal or with a qualified tax professional before submission.

DPDP note: Collect only required tax data, get consent, never store unnecessary copies, and never share PAN/Aadhaar/OTP/password/bank details in chat."""


PAN_GUIDE_CONTEXT_HI = """Source: https://www.incometax.gov.in/iec/foportal/help/all-topics/instant-e-pan/faq
Source: https://www.protean-tinpan.com/services/pan/pan-index.html
Source: https://www.pan.utiitsl.com/PAN/
Service/form: PAN card application / PAN correction through official PAN service portals.

PAN card form भरने की CSC guide:
1. सही PAN service चुनें: new PAN, PAN data correction/change, reprint/reissue, या official portal पर उपलब्ध e-PAN option.
2. Applicant category सावधानी से चुनें: individual, firm, company, trust, HUF या portal में दिखी हुई category.
3. Indian citizen/entity के लिए सामान्यतः Form 49A उपयोग होता है। Foreign citizen/entity के लिए सामान्यतः Form 49AA उपयोग होता है। Correction के लिए correction/change request option चुनें।
4. Name proof document के अनुसार exactly भरें। Surname, first name और middle name applicant document से match होने चाहिए।
5. Father's name/mother's name, date of birth/incorporation, gender और contact details केवल official portal की requirement के अनुसार भरें।
6. Address valid proof के अनुसार भरें। PIN code, state, district और communication address ध्यान से check करें।
7. Aadhaar/PAN/mobile/email जैसी जानकारी केवल official PAN portal में भरें। Aadhaar, PAN number, OTP या document numbers इस chatbot में न डालें।
8. Selected applicant category और mode के अनुसार proof of identity, proof of address और proof of date of birth upload/submit करें।
9. Photo, signature, declaration, consent, payment और acknowledgement final submission से पहले check करें।
10. Submission के बाद acknowledgement number/receipt save करें और status केवल official PAN/service portal पर track करें।

DPDP note: CSC/VLE को केवल वही data collect करना चाहिए जो official PAN portal मांगता है, consent/declaration साफ दिखाना चाहिए, unnecessary copies store नहीं करनी चाहिए, और Aadhaar/PAN/OTP chat में share नहीं करना चाहिए."""


TAX2WIN_GUIDE_CONTEXT_HI = """Source: https://tax2win.in/
Source: https://www.incometax.gov.in/
Service/form: Tax2Win / Income Tax Return filing guidance.

Class 8 level guide: Tax2Win/ITR form कैसे भरें:
1. पहले service confirm करें: income tax return filing, tax calculation, refund tracking, या tax notice/help.
2. शुरू करने से पहले documents तैयार रखें: PAN, Aadhaar अगर official portal मांगे, Form 16, salary slips, bank details, interest certificates, rent/loan details, investment proofs, AIS/TIS, Form 26AS, और deduction proofs.
3. PAN, Aadhaar, bank account number, password या OTP इस chatbot में न लिखें। ऐसी जानकारी केवल official Tax2Win/Income Tax portal में भरें।
4. सही financial year/assessment year चुनें।
5. सही ITR type केवल official portal या tax expert guidance के अनुसार चुनें। Doubt हो तो filing से पहले verify करें।
6. Personal details ध्यान से भरें: name, date of birth, PAN, address, email, mobile और bank details official records से match करें।
7. Income details Form 16, salary slip, interest certificate, business/profession record, capital gains record या official documents से भरें।
8. Deductions/exemptions केवल proof होने पर भरें। Fake deduction न डालें।
9. Tax paid/TDS को Form 26AS/AIS/TIS से match करें।
10. Refund/payable amount, declaration, consent और final summary submit से पहले check करें।
11. Citizen से confirm करने के बाद ही submit करें।
12. Official portal पर e-verification required हो तो पूरा करें।
13. Acknowledgement/ITR-V/reference number save करें और citizen को status track करना बताएं।

Important limitation: Tax filing rules income type, year, documents और law updates पर depend करते हैं। अगर exact field names, ITR type, tax amount या eligibility official source में साफ नहीं है, तो official portal या qualified tax professional से verify करें।

DPDP note: केवल required tax data collect करें, consent लें, unnecessary copies store न करें, और PAN/Aadhaar/OTP/password/bank details chat में share न करें."""


DIGITAL_SEVA_SERVICES_CONTEXT_HI = """Source: https://digitalseva.csc.gov.in/web/services
Service/form group: Digital Seva Portal services.

Official Digital Seva Portal service categories और example services:
- Aadhaar: Aadhaar Demographic Update, Aadhaar Mobile Update, Best Finger Detection, Aadhaar eKYC PVC Print.
- Agriculture: Agricultural Machine Store, Online Store, Farmer Registration, Marketplace.
- Banking and Pension: RAP Registration, Basic Banking Course, Life Certificate (LIC), Pin Pad Device Payment Service.
- Education: SCLM Registration, SCLM Admission, Tally Certification, eLegal Consultancy.
- Election: Punjab Election Services, Uttarakhand Election Services, Meghalaya Election Services, Rajasthan Election Services.
- Electricity: Online Bill Payment (Non-RAPDRP), Online Bill Payment (RAPDRP), Online Bill Payment.
- Government: Birth and Death Application, Forest Services, Online FIR, Ration Card Services.
- Health: Super Speciality Consultation, Telemedicine, Jan Aushadhi Registration, Jiva Telemedicine.
- Insurance: Pradhan Mantri Fasal Bima Yojna, Farmer Package Policy, Life Insurance, Personal Accidental.
- Skills: CAD Registration, Self Animation Course, Digital Unnati, Training Courses.
- Travel: Darshan Booking, Bus Ticket Booking, Flight Tickets, Bus Tickets.
- Others: PVC Card and Biometric Device, Pradhan Mantri Awas Yojana, Jeevan Pramaan, NIELIT Facilitation Centre.

Class 8 level guide: Digital Seva में कोई भी service form कैसे भरें:
1. सबसे पहले service का नाम ध्यान से पढ़ें। वही service चुनें जिसकी citizen को जरूरत है।
2. Digital Seva Portal या CSC द्वारा दिखाए official service page को खोलें।
3. केवल VLE/authorized account से login करें। Password या OTP किसी को न बताएं।
4. Form भरने से पहले required documents तैयार रखें। Documents service के हिसाब से बदल सकते हैं।
5. Citizen का data भरने से पहले consent लें।
6. Basic details धीरे-धीरे भरें: name, date, address, mobile, category, location और बाकी fields citizen के documents के अनुसार भरें।
7. अगर form ID number मांगता है, तो उसे केवल official portal में भरें। Aadhaar, PAN, bank details, OTP या document number इस chatbot में न लिखें।
8. केवल वही documents upload करें जो official portal मांगता है। File size, photo clarity और document type check करें।
9. Submit करने से पहले spelling, numbers, district, state, dates और uploaded files दोबारा check करें।
10. अगर payment required है, तो payment केवल official portal पर करें।
11. Acknowledgement, receipt, application number या reference number save/print करें।
12. Citizen को बताएं कि status official portal/helpdesk पर कैसे track करना है।

Important limitation: Digital Seva services page services और categories बताता है, लेकिन exact fields, fee, eligibility और document list हर service में अलग हो सकती है। अगर कोई field/document indexed official source में नहीं है, तो final submission से पहले official Digital Seva/service portal में verify करें।

DPDP note: केवल service के लिए जरूरी data collect करें, consent साफ बताएं, documents सुरक्षित रखें, और unnecessary personal data store/share न करें."""


def _dsp_enhancement_context(service_title, language="en"):

    if language == "hi":
        return f"""Who Can Use:
Authorized CSC/VLE account या वह role जिसे Digital Seva Portal में यह service enabled दिखती है। Exact access role portal में service के अंदर दिखता है।

Prerequisites:
- Active Digital Seva Portal login.
- Citizen consent before entering personal details.
- Required documents and payment method ready if the official service asks.
- Working biometric/device/OTP flow only when the service requires it.

DSP Navigation:
1. Digital Seva Portal login page खोलें।
2. Authorized CSC/VLE credentials से login करें।
3. Service search या category list में {service_title} से related exact service खोजें।
4. Service instructions, role access, fee, documents और consent/declaration पढ़ें।
5. अगर portal official department/provider page पर redirect करता है, तो आगे की entry केवल उसी official page पर करें।

Form Filling Guide:
1. Service name और citizen की जरूरत match करें।
2. Citizen details official documents के अनुसार भरें।
3. Aadhaar, PAN, bank details, OTP, health या child/minor data केवल official portal field में भरें, chat में नहीं।
4. Required dropdown, category, location, date, mobile और address fields सावधानी से भरें।
5. Documents केवल portal में मांगे गए format, size और type में upload करें।
6. Submit से पहले spelling, numbers, document upload, fee, consent और declaration check करें।

Application Workflow:
1. Draft/details review करें।
2. Validate/verify button हो तो use करें।
3. Payment required हो तो official portal/payment page पर pay करें।
4. Submit के बाद application number, acknowledgement, receipt या transaction ID save करें।

Status Tracking:
Application/reference/receipt number से same DSP service, status option, official department portal या helpdesk पर status track करें, जैसा portal में दिखे।

Approval Process:
Approval department/provider workflow पर depend करता है। Timeline या approval guarantee तभी बताएं जब official portal/SOP में साफ लिखा हो।

Download / Print:
Submission या approval के बाद receipt, acknowledgement, certificate, ticket, policy, order या form download/print option portal में दिखे तो use करें।

Common Errors:
- Service not enabled for role/location: VLE authorization, state, category और service availability check करें।
- Required field missing: लाल/mandatory field complete करें।
- Invalid document/file: correct document type, clear scan/photo और allowed size upload करें।
- Name/date/address mismatch: citizen document के साथ match करें।
- Payment pending/failed: transaction status check करें; duplicate payment blindly न करें।
- OTP/biometric/device failure: OTP share न करें; official portal/device screen पर retry करें।"""

    return f"""Who Can Use:
Authorized CSC/VLE account or the role for which this service is enabled inside the Digital Seva Portal. Exact access role is shown inside the portal/service.

Prerequisites:
- Active Digital Seva Portal login.
- Citizen consent before entering personal details.
- Required documents and payment method ready if the official service asks.
- Working biometric/device/OTP flow only when the service requires it.

DSP Navigation:
1. Open the Digital Seva Portal login page.
2. Login with authorized CSC/VLE credentials.
3. Use service search or the category list to find the exact service related to {service_title}.
4. Read service instructions, role access, fee, documents, and consent/declaration.
5. If the portal redirects to an official department/provider page, continue only on that official page.

Form Filling Guide:
1. Match the service name with the citizen's need.
2. Fill citizen details exactly as shown in official documents.
3. Enter Aadhaar, PAN, bank details, OTP, health, or child/minor data only in the official portal field, not in chat.
4. Fill required dropdowns, category, location, date, mobile, and address fields carefully.
5. Upload documents only in the format, size, and type asked by the portal.
6. Before submit, check spelling, numbers, document upload, fee, consent, and declaration.

Application Workflow:
1. Review draft/details.
2. Use Validate/Verify if the service shows that button.
3. Pay fee only on the official portal/payment page if required.
4. After submission, save application number, acknowledgement, receipt, or transaction ID.

Status Tracking:
Track status with the application/reference/receipt number in the same DSP service, status option, official department portal, or helpdesk as shown by the portal.

Approval Process:
Approval depends on the department/provider workflow. Do not promise timeline or approval unless the official portal/SOP clearly states it.

Download / Print:
After submission or approval, use the receipt, acknowledgement, certificate, ticket, policy, order, or form download/print option if the portal shows it.

Common Errors:
- Service not enabled for role/location: check VLE authorization, state, category, and service availability.
- Required field missing: complete the red/mandatory field.
- Invalid document/file: upload the correct document type, clear scan/photo, and allowed file size.
- Name/date/address mismatch: match details with citizen documents.
- Payment pending/failed: check transaction status; do not make duplicate payment blindly.
- OTP/biometric/device failure: do not share OTP; retry only on the official portal/device screen."""


PAN_DSP_CONTEXT = """Who Can Use:
Citizen/entity applying through an authorized CSC/VLE account or official PAN service portal flow.

Prerequisites:
- Correct PAN service choice: new PAN, correction/change, reprint/reissue, or e-PAN if available.
- Proof of identity, proof of address, and proof of date of birth as applicable.
- Citizen consent, photo/signature, and payment method if required.

DSP Navigation:
1. Login to Digital Seva Portal with authorized CSC/VLE credentials.
2. Search/select PAN service if it is enabled in the account.
3. Choose new PAN, correction/change, reprint/reissue, or e-PAN as required.
4. If redirected to Protean/UTIITSL/Income Tax official PAN page, continue only on that official page.

Form Filling Guide:
1. Select applicant category and correct form/mode shown by the official PAN portal.
2. Fill name, date of birth/incorporation, gender, parent name, address, mobile/email, photo, and signature as required.
3. Enter Aadhaar/PAN/contact/document numbers only inside the official PAN portal.
4. Upload/submit identity, address, and date-of-birth proof as required.
5. Review declaration, consent, fee/payment, and acknowledgement before final submit.

Application Workflow:
1. Complete the form on the official PAN flow.
2. Validate details and upload documents.
3. Pay fee if required.
4. Submit and save acknowledgement/receipt.

Status Tracking:
Track status using the acknowledgement/reference number on the official PAN/service portal.

Download / Print:
Download/print acknowledgement, receipt, e-PAN, or submitted form only when the official portal provides the option.

Common Errors:
- Name mismatch: match the proof document exactly.
- Wrong applicant category: correct category before submission.
- Invalid photo/signature/document: upload as per portal requirement.
- Payment failed: check official payment/transaction status before retrying.

Comparison:
- PAN correction/change is used when existing PAN details need correction or update.
- PAN reprint/reissue is used when PAN card copy is needed again and PAN data is not being changed.
- New PAN is for an applicant who does not already have PAN.
- Select the option shown by the official PAN portal and citizen requirement before payment/submission."""


PAN_DSP_CONTEXT_HI = """Who Can Use:
Authorized CSC/VLE account या official PAN service portal flow से apply करने वाला citizen/entity.

Prerequisites:
- सही PAN service choice: new PAN, correction/change, reprint/reissue, या e-PAN अगर available हो।
- Proof of identity, proof of address और proof of date of birth, जैसा applicable हो।
- Citizen consent, photo/signature और payment method अगर required हो।

DSP Navigation:
1. Authorized CSC/VLE credentials से Digital Seva Portal login करें।
2. Account में enabled हो तो PAN service search/select करें।
3. जरूरत के अनुसार new PAN, correction/change, reprint/reissue या e-PAN चुनें।
4. Protean/UTIITSL/Income Tax official PAN page पर redirect हो तो entry केवल उसी official page पर करें।

Form Filling Guide:
1. Official PAN portal में applicant category और सही form/mode चुनें।
2. Name, date of birth/incorporation, gender, parent name, address, mobile/email, photo और signature required अनुसार भरें।
3. Aadhaar/PAN/contact/document numbers केवल official PAN portal में भरें।
4. Identity, address और date-of-birth proof required अनुसार upload/submit करें।
5. Final submit से पहले declaration, consent, fee/payment और acknowledgement check करें।

Application Workflow:
1. Official PAN flow पर form complete करें।
2. Details validate करें और documents upload करें।
3. Required हो तो fee pay करें।
4. Submit करके acknowledgement/receipt save करें।

Status Tracking:
Official PAN/service portal पर acknowledgement/reference number से status track करें।

Download / Print:
Official portal option दे तो acknowledgement, receipt, e-PAN या submitted form download/print करें।

Common Errors:
- Name mismatch: proof document से exact match करें।
- Wrong applicant category: submission से पहले correct category चुनें।
- Invalid photo/signature/document: portal requirement के अनुसार upload करें।
- Payment failed: retry से पहले official transaction status check करें।

Comparison:
- PAN correction/change तब use करें जब existing PAN details में correction/update चाहिए।
- PAN reprint/reissue तब use करें जब PAN card copy फिर चाहिए और PAN data change नहीं करना है।
- New PAN उस applicant के लिए है जिसके पास पहले से PAN नहीं है।
- Payment/submission से पहले official PAN portal में दिखा option और citizen requirement match करें।"""


TAX_DSP_CONTEXT = """Who Can Use:
Citizen filing income tax return through an authorized tax filing service or official Income Tax portal flow.

Prerequisites:
- Correct financial year/assessment year.
- PAN, Aadhaar if required by the official portal, Form 16, AIS/TIS, Form 26AS, income proofs, bank details, and deduction proofs as applicable.
- Citizen consent and access to official e-verification method if required.

DSP Navigation:
1. Login to Digital Seva Portal with authorized credentials if using a CSC-enabled tax service.
2. Search/select the income tax/ITR/tax filing service if enabled.
3. If redirected to Tax2Win or Income Tax official portal, continue only on that official page.
4. Select the correct tax filing service/year shown by the official portal.

Form Filling Guide:
1. Select financial year/assessment year.
2. Select ITR type only as guided by the official portal or tax expert.
3. Fill personal, income, tax paid/TDS, deduction, bank, and declaration details from official records.
4. Do not enter PAN, Aadhaar, password, OTP, or bank details in chat.
5. Review tax payable/refund, declaration, consent, and final summary before submit.

Application Workflow:
1. Prepare documents.
2. Fill return on the official tax flow.
3. Submit only after citizen confirms.
4. Complete e-verification if required.
5. Save acknowledgement/ITR-V/reference number.

Status Tracking:
Track return, refund, or e-verification status only on the official tax/service portal.

Download / Print:
Download/print acknowledgement, ITR-V, computation, or filed return only from the official portal if available.

Common Errors:
- Wrong year or ITR type: verify before filing.
- TDS mismatch: check Form 26AS/AIS/TIS.
- Fake/unsupported deduction: use only valid proof.
- E-verification pending: complete it on the official portal."""


TAX_DSP_CONTEXT_HI = """Who Can Use:
Authorized tax filing service या official Income Tax portal flow से ITR file करने वाला citizen.

Prerequisites:
- सही financial year/assessment year.
- PAN, Aadhaar अगर official portal मांगे, Form 16, AIS/TIS, Form 26AS, income proofs, bank details और deduction proofs जैसा applicable हो।
- Citizen consent और required हो तो official e-verification access.

DSP Navigation:
1. CSC-enabled tax service use कर रहे हैं तो authorized credentials से Digital Seva Portal login करें।
2. Enabled हो तो income tax/ITR/tax filing service search/select करें।
3. Tax2Win या Income Tax official portal पर redirect हो तो entry केवल उसी official page पर करें।
4. Official portal में सही tax filing service/year चुनें।

Form Filling Guide:
1. Financial year/assessment year चुनें।
2. ITR type केवल official portal या tax expert guidance के अनुसार चुनें।
3. Personal, income, tax paid/TDS, deduction, bank और declaration details official records से भरें।
4. PAN, Aadhaar, password, OTP या bank details chat में न डालें।
5. Submit से पहले tax payable/refund, declaration, consent और final summary review करें।

Application Workflow:
1. Documents तैयार करें।
2. Official tax flow पर return भरें।
3. Citizen confirmation के बाद submit करें।
4. Required हो तो e-verification पूरा करें।
5. Acknowledgement/ITR-V/reference number save करें।

Status Tracking:
Return, refund या e-verification status केवल official tax/service portal पर track करें।

Download / Print:
Official portal available कराए तो acknowledgement, ITR-V, computation या filed return download/print करें।

Common Errors:
- Wrong year या ITR type: filing से पहले verify करें।
- TDS mismatch: Form 26AS/AIS/TIS check करें।
- Fake/unsupported deduction: केवल valid proof use करें।
- E-verification pending: official portal पर पूरा करें।"""


DIGITAL_SEVA_CATEGORY_GUIDES_EN = {
    "aadhaar": {
        "title": "Aadhaar services",
        "examples": (
            "Aadhaar Demographic Update",
            "Aadhaar Mobile Update",
            "Best Finger Detection",
            "Aadhaar eKYC PVC Print",
        ),
        "fields": (
            "Service type: choose demographic update, mobile update, best finger detection, or Aadhaar eKYC PVC print as shown by the portal.",
            "Resident details: fill name, date of birth/age, gender, address, mobile/email only when the official form asks.",
            "Aadhaar/VID/biometric details: enter them only inside the official portal/device screen, never in this chat.",
            "Consent/declaration: explain why the data is needed and take clear citizen consent before submission.",
            "Proof/device/payment: upload documents, capture biometric/device result, or complete payment only if the official service asks.",
            "Final check: verify spelling, mobile number, address, uploaded file, consent, and acknowledgement number.",
        ),
        "summary": "select the exact Aadhaar service, fill resident details only on the official screen, verify consent/biometric/upload/payment, and save acknowledgement.",
    },
    "agriculture": {
        "title": "Agriculture services",
        "examples": (
            "Agricultural Machine Store",
            "Online Store",
            "Farmer Registration",
            "Marketplace",
        ),
        "fields": (
            "Service type: choose farmer registration, machine store, online store, or marketplace service.",
            "Farmer/customer details: fill name, mobile, state, district, village, address, and category only as required.",
            "Farm/service details: fill crop, land, machinery, product, quantity, delivery, or marketplace details shown on the form.",
            "Documents: upload land/farmer/category/address documents only if the official service asks.",
            "Payment/order: confirm price, subsidy, fee, quantity, address, and payment status before submit.",
            "Receipt: save registration/order/reference number and explain status tracking to the farmer.",
        ),
        "summary": "identify the farmer/service, fill location and crop/product details, check documents/payment, and save the registration or order reference.",
    },
    "banking_pension": {
        "title": "Banking and pension services",
        "examples": (
            "RAP Registration",
            "Basic Banking Course",
            "Life Certificate (LIC)",
            "Pin Pad Device Payment Service",
        ),
        "fields": (
            "Service type: choose banking course, RAP registration, life certificate, pin pad/device payment, or pension-related service.",
            "Applicant/pensioner details: fill name, mobile, address, age/date of birth, pension/customer details only inside the official portal.",
            "Bank/pension fields: enter account/customer/policy/pension details only when the official form asks and only on the portal.",
            "Verification: complete biometric, device, OTP, or declaration step only on the official portal/device.",
            "Documents/payment: upload proof or pay fee/premium only if the official service asks.",
            "Receipt: save transaction ID, certificate number, acknowledgement, or course/reference number.",
        ),
        "summary": "choose the banking/pension service, fill applicant details, complete official verification, and save the certificate or transaction reference.",
    },
    "education": {
        "title": "Education services",
        "examples": (
            "SCLM Registration",
            "SCLM Admission",
            "Tally Certification",
            "eLegal Consultancy",
        ),
        "fields": (
            "Service type: choose registration, admission, certification, course, or consultancy service.",
            "Student/learner details: fill name, date of birth, class/qualification, mobile/email, address, and category as asked.",
            "Course/admission details: select course, batch, centre, subject, admission type, or exam/certificate option.",
            "Guardian/minor care: for children or school students, collect guardian consent and do not share child data in chat.",
            "Documents/payment: upload marksheet, photo, ID, category proof, or fee receipt only if required.",
            "Receipt: save admission, enrollment, certificate, or consultation reference number.",
        ),
        "summary": "select the course/admission service, fill learner details, handle minor data carefully, upload required documents, and save enrollment reference.",
    },
    "election": {
        "title": "Election services",
        "examples": (
            "Punjab Election Services",
            "Uttarakhand Election Services",
            "Meghalaya Election Services",
            "Rajasthan Election Services",
        ),
        "fields": (
            "Service type: choose new voter service, correction, download, search, or state election service shown on the portal.",
            "Applicant details: fill name, age/date of birth, gender, mobile, address, district, assembly/constituency as asked.",
            "Voter fields: enter EPIC/voter ID only inside the official election service portal when required.",
            "Documents: upload age, address, photo, or correction proof only if the official form asks.",
            "Declaration: review citizen declaration and state/district details carefully before submission.",
            "Receipt: save application/reference number and tell the citizen how to track status.",
        ),
        "summary": "choose the correct election service/state, fill voter/applicant details, upload proof if asked, and save the application reference.",
    },
    "electricity": {
        "title": "Electricity bill services",
        "examples": (
            "Online Bill Payment (Non-RAPDRP)",
            "Online Bill Payment (RAPDRP)",
            "Online Bill Payment",
        ),
        "fields": (
            "Service type: choose the electricity bill payment option and correct biller/discom/state.",
            "Consumer details: enter consumer number, account number, or bill number only inside the official payment portal.",
            "Bill check: verify consumer name, bill amount, due date, arrears, and service charge before payment.",
            "Contact/payment: fill mobile/email and complete payment only on the official portal/payment page.",
            "Final confirmation: do not submit if consumer name or bill amount does not match the citizen's bill.",
            "Receipt: save payment receipt, transaction ID, and bill reference number.",
        ),
        "summary": "select biller/discom, enter consumer number only on the official page, verify amount/name, pay safely, and save receipt.",
    },
    "government": {
        "title": "Government services",
        "examples": (
            "Birth and Death Application",
            "Forest Services",
            "Online FIR",
            "Ration Card Services",
        ),
        "fields": (
            "Service type: choose the exact government service such as birth/death, forest, FIR, ration card, certificate, or application service.",
            "Applicant/citizen details: fill name, mobile, address, family details, location, district, and category only as asked.",
            "Event/service details: fill birth/death, FIR, ration, certificate, or department-specific fields from official documents.",
            "Documents: upload proof of identity, address, relationship, event, or category only if the official form asks.",
            "Declaration: read the declaration to the citizen and submit only after confirmation.",
            "Receipt: save acknowledgement/application number and explain tracking or department follow-up.",
        ),
        "summary": "choose the exact government service, fill citizen and event details from documents, upload required proof, and save acknowledgement.",
    },
    "health": {
        "title": "Health services",
        "examples": (
            "Super Speciality Consultation",
            "Telemedicine",
            "Jan Aushadhi Registration",
            "Jiva Telemedicine",
        ),
        "fields": (
            "Service type: choose telemedicine, consultation, medicine, registration, or health service shown by the portal.",
            "Patient details: fill name, age, gender, mobile, address, and appointment/service details only as required.",
            "Health information: enter symptoms, reports, prescription, or medicine details only inside the official health service screen.",
            "Consent/privacy: take consent before sharing health information with doctor/service provider.",
            "Appointment/payment: confirm doctor/service, date/time, fee, medicine/order details, and payment if required.",
            "Receipt: save appointment ID, consultation reference, prescription, or order number.",
        ),
        "summary": "select health service, fill patient and appointment details privately, upload reports only if asked, and save consultation/order reference.",
    },
    "insurance": {
        "title": "Insurance services",
        "examples": (
            "Pradhan Mantri Fasal Bima Yojna",
            "Farmer Package Policy",
            "Life Insurance",
            "Personal Accidental",
        ),
        "fields": (
            "Service type: choose crop insurance, farmer package, life insurance, personal accidental, or other insurance service.",
            "Applicant details: fill name, age/date of birth, mobile, address, occupation/farmer details only as asked.",
            "Policy details: fill nominee, crop/land, sum insured, premium, policy term, and risk details only on the official portal.",
            "Documents: upload identity, address, crop/land, bank, nominee, or age proof only when required.",
            "Consent/disclosure: explain declaration, premium, coverage, exclusions, and claim basics from the official screen.",
            "Receipt: save policy number, proposal number, payment receipt, or acknowledgement.",
        ),
        "summary": "choose insurance type, fill applicant/policy details only from documents, review consent and premium, and save policy/reference number.",
    },
    "skills": {
        "title": "Skill services",
        "examples": (
            "CAD Registration",
            "Self Animation Course",
            "Digital Unnati",
            "Training Courses",
        ),
        "fields": (
            "Service type: choose registration, course, training, CAD, animation, Digital Unnati, or certificate service.",
            "Learner details: fill name, date of birth, mobile/email, address, education/qualification, and category as asked.",
            "Course details: select course name, centre, batch, language, schedule, fee, and training mode.",
            "Documents: upload photo, ID, qualification, or category proof only if the portal asks.",
            "Consent/payment: confirm course details, fee, declaration, and payment before final submit.",
            "Receipt: save registration/enrollment/certificate/reference number.",
        ),
        "summary": "select the skill course, fill learner and batch details, upload required proof, pay if asked, and save enrollment reference.",
    },
    "travel": {
        "title": "Travel services",
        "examples": (
            "Darshan Booking",
            "Bus Ticket Booking",
            "Flight Tickets",
            "Bus Tickets",
        ),
        "fields": (
            "Service type: choose darshan booking, bus ticket, flight ticket, or travel service.",
            "Journey details: fill from, to, date, time, route, seat/class, passenger count, and fare shown by the portal.",
            "Passenger details: enter name, age, gender, mobile/email, and ID details only inside the official booking portal if asked.",
            "Review: check spelling, journey date, route, passenger count, cancellation rule, and fare before payment.",
            "Payment: complete payment only on the official travel/payment page.",
            "Ticket: save ticket, PNR/booking ID, receipt, and travel instructions.",
        ),
        "summary": "choose travel type, fill journey/passenger details on the official page, review fare/date, pay safely, and save ticket/PNR.",
    },
    "others": {
        "title": "Other CSC services",
        "examples": (
            "PVC Card and Biometric Device",
            "Pradhan Mantri Awas Yojana",
            "Jeevan Pramaan",
            "NIELIT Facilitation Centre",
        ),
        "fields": (
            "Service type: first identify the exact service, because 'Others' includes very different services.",
            "Applicant details: fill name, mobile, address, location, category, and service-specific details as shown by the portal.",
            "Service details: fill PVC/device, PMAY, Jeevan Pramaan, NIELIT, certificate, or facilitation fields only from official documents.",
            "Verification: complete biometric, OTP, device, declaration, or document verification only on the official portal/device.",
            "Documents/payment: upload documents and pay fee only when the official service asks.",
            "Receipt: save acknowledgement, certificate, application, transaction, or facilitation reference number.",
        ),
        "summary": "identify the exact 'Other' service first, fill applicant/service details from documents, complete official verification, and save reference.",
    },
}


DIGITAL_SEVA_CATEGORY_GUIDES_HI = {
    "aadhaar": {
        "title": "Aadhaar services",
        "examples": DIGITAL_SEVA_CATEGORY_GUIDES_EN["aadhaar"]["examples"],
        "fields": (
            "Service type: portal में दिखी Aadhaar demographic update, mobile update, best finger detection या Aadhaar eKYC PVC print service चुनें।",
            "Resident details: name, date of birth/age, gender, address, mobile/email केवल official form मांगने पर भरें।",
            "Aadhaar/VID/biometric details: इन्हें केवल official portal/device screen में भरें, इस chat में कभी नहीं।",
            "Consent/declaration: citizen को data use का कारण बताकर साफ consent लें।",
            "Proof/device/payment: document upload, biometric/device result या payment केवल official service मांगने पर करें।",
            "Final check: spelling, mobile number, address, uploaded file, consent और acknowledgement number check करें।",
        ),
        "summary": "exact Aadhaar service चुनें, resident details केवल official screen पर भरें, consent/biometric/upload/payment check करें, और acknowledgement save करें।",
    },
    "agriculture": {
        "title": "Agriculture services",
        "examples": DIGITAL_SEVA_CATEGORY_GUIDES_EN["agriculture"]["examples"],
        "fields": (
            "Service type: farmer registration, machine store, online store या marketplace service चुनें।",
            "Farmer/customer details: name, mobile, state, district, village, address और category official form के अनुसार भरें।",
            "Farm/service details: crop, land, machinery, product, quantity, delivery या marketplace details form में दिखे अनुसार भरें।",
            "Documents: land/farmer/category/address document केवल official service मांगने पर upload करें।",
            "Payment/order: price, subsidy, fee, quantity, address और payment status submit से पहले check करें।",
            "Receipt: registration/order/reference number save करें और farmer को status tracking बताएं।",
        ),
        "summary": "farmer/service पहचानें, location और crop/product details भरें, documents/payment check करें, और registration/order reference save करें।",
    },
    "banking_pension": {
        "title": "Banking and pension services",
        "examples": DIGITAL_SEVA_CATEGORY_GUIDES_EN["banking_pension"]["examples"],
        "fields": (
            "Service type: banking course, RAP registration, life certificate, pin pad/device payment या pension service चुनें।",
            "Applicant/pensioner details: name, mobile, address, age/date of birth, pension/customer details केवल official portal में भरें।",
            "Bank/pension fields: account/customer/policy/pension details केवल official form मांगने पर portal में ही भरें।",
            "Verification: biometric, device, OTP या declaration step केवल official portal/device पर पूरा करें।",
            "Documents/payment: proof upload या fee/premium payment केवल official service मांगने पर करें।",
            "Receipt: transaction ID, certificate number, acknowledgement या course/reference number save करें।",
        ),
        "summary": "banking/pension service चुनें, applicant details भरें, official verification पूरा करें, और certificate/transaction reference save करें।",
    },
    "education": {
        "title": "Education services",
        "examples": DIGITAL_SEVA_CATEGORY_GUIDES_EN["education"]["examples"],
        "fields": (
            "Service type: registration, admission, certification, course या consultancy service चुनें।",
            "Student/learner details: name, date of birth, class/qualification, mobile/email, address और category form के अनुसार भरें।",
            "Course/admission details: course, batch, centre, subject, admission type या exam/certificate option चुनें।",
            "Guardian/minor care: बच्चे/student के लिए guardian consent लें और child data chat में share न करें।",
            "Documents/payment: marksheet, photo, ID, category proof या fee receipt केवल required हो तो upload करें।",
            "Receipt: admission, enrollment, certificate या consultation reference number save करें।",
        ),
        "summary": "course/admission service चुनें, learner details भरें, minor data संभालकर रखें, documents upload करें, और enrollment reference save करें।",
    },
    "election": {
        "title": "Election services",
        "examples": DIGITAL_SEVA_CATEGORY_GUIDES_EN["election"]["examples"],
        "fields": (
            "Service type: new voter, correction, download, search या state election service portal में दिखे अनुसार चुनें।",
            "Applicant details: name, age/date of birth, gender, mobile, address, district, assembly/constituency form के अनुसार भरें।",
            "Voter fields: EPIC/voter ID केवल official election service portal में required होने पर भरें।",
            "Documents: age, address, photo या correction proof केवल official form मांगने पर upload करें।",
            "Declaration: citizen declaration और state/district details submit से पहले ध्यान से check करें।",
            "Receipt: application/reference number save करें और citizen को status tracking बताएं।",
        ),
        "summary": "correct election service/state चुनें, voter/applicant details भरें, proof upload करें, और application reference save करें।",
    },
    "electricity": {
        "title": "Electricity bill services",
        "examples": DIGITAL_SEVA_CATEGORY_GUIDES_EN["electricity"]["examples"],
        "fields": (
            "Service type: electricity bill payment option और सही biller/discom/state चुनें।",
            "Consumer details: consumer number, account number या bill number केवल official payment portal में भरें।",
            "Bill check: consumer name, bill amount, due date, arrears और service charge payment से पहले verify करें।",
            "Contact/payment: mobile/email भरें और payment केवल official portal/payment page पर करें।",
            "Final confirmation: अगर consumer name या amount bill से match नहीं करता, तो submit न करें।",
            "Receipt: payment receipt, transaction ID और bill reference number save करें।",
        ),
        "summary": "biller/discom चुनें, consumer number official page पर भरें, amount/name verify करें, payment करें, और receipt save करें।",
    },
    "government": {
        "title": "Government services",
        "examples": DIGITAL_SEVA_CATEGORY_GUIDES_EN["government"]["examples"],
        "fields": (
            "Service type: birth/death, forest, FIR, ration card, certificate या application service जैसे exact service चुनें।",
            "Applicant/citizen details: name, mobile, address, family details, location, district और category form के अनुसार भरें।",
            "Event/service details: birth/death, FIR, ration, certificate या department-specific fields official documents से भरें।",
            "Documents: identity, address, relationship, event या category proof केवल official form मांगने पर upload करें।",
            "Declaration: declaration citizen को पढ़कर/समझाकर submit से पहले confirm करें।",
            "Receipt: acknowledgement/application number save करें और tracking/follow-up बताएं।",
        ),
        "summary": "exact government service चुनें, citizen और event details documents से भरें, required proof upload करें, और acknowledgement save करें।",
    },
    "health": {
        "title": "Health services",
        "examples": DIGITAL_SEVA_CATEGORY_GUIDES_EN["health"]["examples"],
        "fields": (
            "Service type: telemedicine, consultation, medicine, registration या health service चुनें।",
            "Patient details: name, age, gender, mobile, address और appointment/service details required होने पर भरें।",
            "Health information: symptoms, reports, prescription या medicine details केवल official health service screen में भरें।",
            "Consent/privacy: doctor/service provider के साथ health information share करने से पहले consent लें।",
            "Appointment/payment: doctor/service, date/time, fee, medicine/order details और payment check करें।",
            "Receipt: appointment ID, consultation reference, prescription या order number save करें।",
        ),
        "summary": "health service चुनें, patient और appointment details privacy के साथ भरें, reports required हों तो upload करें, और consultation/order reference save करें।",
    },
    "insurance": {
        "title": "Insurance services",
        "examples": DIGITAL_SEVA_CATEGORY_GUIDES_EN["insurance"]["examples"],
        "fields": (
            "Service type: crop insurance, farmer package, life insurance, personal accidental या other insurance service चुनें।",
            "Applicant details: name, age/date of birth, mobile, address, occupation/farmer details form के अनुसार भरें।",
            "Policy details: nominee, crop/land, sum insured, premium, policy term और risk details केवल official portal में भरें।",
            "Documents: identity, address, crop/land, bank, nominee या age proof required होने पर upload करें।",
            "Consent/disclosure: declaration, premium, coverage, exclusions और claim basics official screen से समझाएं।",
            "Receipt: policy number, proposal number, payment receipt या acknowledgement save करें।",
        ),
        "summary": "insurance type चुनें, applicant/policy details documents से भरें, consent और premium review करें, और policy/reference number save करें।",
    },
    "skills": {
        "title": "Skill services",
        "examples": DIGITAL_SEVA_CATEGORY_GUIDES_EN["skills"]["examples"],
        "fields": (
            "Service type: registration, course, training, CAD, animation, Digital Unnati या certificate service चुनें।",
            "Learner details: name, date of birth, mobile/email, address, education/qualification और category form के अनुसार भरें।",
            "Course details: course name, centre, batch, language, schedule, fee और training mode चुनें।",
            "Documents: photo, ID, qualification या category proof केवल portal मांगने पर upload करें।",
            "Consent/payment: course details, fee, declaration और payment final submit से पहले confirm करें।",
            "Receipt: registration/enrollment/certificate/reference number save करें।",
        ),
        "summary": "skill course चुनें, learner और batch details भरें, required proof upload करें, fee required हो तो pay करें, और enrollment reference save करें।",
    },
    "travel": {
        "title": "Travel services",
        "examples": DIGITAL_SEVA_CATEGORY_GUIDES_EN["travel"]["examples"],
        "fields": (
            "Service type: darshan booking, bus ticket, flight ticket या travel service चुनें।",
            "Journey details: from, to, date, time, route, seat/class, passenger count और fare portal के अनुसार भरें।",
            "Passenger details: name, age, gender, mobile/email और ID details required होने पर official booking portal में भरें।",
            "Review: spelling, journey date, route, passenger count, cancellation rule और fare payment से पहले check करें।",
            "Payment: payment केवल official travel/payment page पर करें।",
            "Ticket: ticket, PNR/booking ID, receipt और travel instructions save करें।",
        ),
        "summary": "travel type चुनें, journey/passenger details official page पर भरें, fare/date review करें, payment करें, और ticket/PNR save करें।",
    },
    "others": {
        "title": "Other CSC services",
        "examples": DIGITAL_SEVA_CATEGORY_GUIDES_EN["others"]["examples"],
        "fields": (
            "Service type: पहले exact service पहचानें, क्योंकि 'Others' में अलग-अलग services होती हैं।",
            "Applicant details: name, mobile, address, location, category और service-specific details portal के अनुसार भरें।",
            "Service details: PVC/device, PMAY, Jeevan Pramaan, NIELIT, certificate या facilitation fields official documents से भरें।",
            "Verification: biometric, OTP, device, declaration या document verification केवल official portal/device पर करें।",
            "Documents/payment: documents upload और fee payment केवल official service मांगने पर करें।",
            "Receipt: acknowledgement, certificate, application, transaction या facilitation reference number save करें।",
        ),
        "summary": "exact 'Other' service पहले पहचानें, applicant/service details documents से भरें, official verification पूरा करें, और reference save करें।",
    },
}


DIGITAL_SEVA_CATEGORY_KEYWORDS = (
    ("aadhaar", ("aadhaar", "aadhar", "uidai", "आधार")),
    ("agriculture", ("agriculture", "agricultural", "farmer", "crop", "machine store", "marketplace", "agri", "कृषि", "किसान", "फसल")),
    ("banking_pension", ("banking", "bank", "pension", "life certificate", "jeevan pramaan", "rap registration", "pin pad", "basic banking", "बैंक", "पेंशन", "जीवन प्रमाण")),
    ("education", ("education", "student", "school", "admission", "course", "tally", "elegal", "sclm", "शिक्षा", "स्कूल", "एडमिशन", "कोर्स")),
    ("election", ("election", "voter", "epic", "vote", "voter id", "punjab election", "uttarakhand election", "meghalaya election", "rajasthan election", "चुनाव", "वोटर", "मतदाता")),
    ("electricity", ("electricity", "electric bill", "bijli", "bill payment", "discom", "rapdrp", "बिजली", "बिल")),
    ("government", ("government", "birth", "death", "forest", "fir", "ration", "certificate", "govt", "सरकारी", "जन्म", "मृत्यु", "राशन")),
    ("health", ("health", "telemedicine", "consultation", "jan aushadhi", "jiva", "doctor", "medicine", "स्वास्थ्य", "टेलीमेडिसिन", "दवाई", "डॉक्टर")),
    ("insurance", ("insurance", "bima", "fasal bima", "life insurance", "accidental", "policy", "premium", "बीमा", "पॉलिसी")),
    ("skills", ("skill", "skills", "training", "cad", "animation", "digital unnati", "कौशल", "ट्रेनिंग")),
    ("travel", ("travel", "darshan", "bus ticket", "flight", "ticket booking", "pnr", "यात्रा", "बस", "फ्लाइट", "टिकट")),
    ("others", ("other csc", "others", "other services", "pvc card", "biometric device", "pmay", "awas", "nielit", "other form", "अन्य", "पीवीसी", "आवास")),
)


def _numbered_lines(items):

    return "\n".join(f"{index}. {item}" for index, item in enumerate(items, start=1))


def _category_context(category, language="en"):

    if language == "hi":
        data = DIGITAL_SEVA_CATEGORY_GUIDES_HI[category]
        examples = "\n".join(f"- {item}" for item in data["examples"])
        fields = _numbered_lines(data["fields"])
        return f"""Source: https://digitalseva.csc.gov.in/web/services
Service/form group: {data["title"]}.

Official Digital Seva example services:
{examples}

Class 8 level guide: {data["title"]} form कैसे भरें:
{fields}

Important limitation: Digital Seva services page category और example services बताता है। Exact field names, fee, eligibility और document list हर service में अलग हो सकती है। अगर exact detail indexed/official source में नहीं है, तो final submission से पहले official Digital Seva/service portal में verify करें।

DPDP note: Aadhaar, PAN, bank details, OTP, password, health data या child/minor personal data इस chat में न डालें। ऐसी जानकारी केवल official CSC/service portal में भरें।

{_dsp_enhancement_context(data["title"], "hi")}"""

    data = DIGITAL_SEVA_CATEGORY_GUIDES_EN[category]
    examples = "\n".join(f"- {item}" for item in data["examples"])
    fields = _numbered_lines(data["fields"])
    return f"""Source: https://digitalseva.csc.gov.in/web/services
Service/form group: {data["title"]}.

Official Digital Seva example services:
{examples}

Class 8 level guide to fill {data["title"]} forms:
{fields}

Important limitation: The Digital Seva services page confirms the category and example services. Exact field names, fee, eligibility, and document list can be different for each service. If exact details are not available from indexed/official source data, verify them inside the official Digital Seva/service portal before final submission.

DPDP note: Do not paste Aadhaar, PAN, bank details, OTP, passwords, health data, or child/minor personal data in this chat. Enter those only inside the official CSC/service portal.

{_dsp_enhancement_context(data["title"], "en")}"""


def _category_summary(language="en"):

    if language == "hi":
        lines = [
            f"- {data['title']}: {data['summary']}"
            for data in DIGITAL_SEVA_CATEGORY_GUIDES_HI.values()
        ]
        return (
            "Category-wise safe guidance for Digital Seva forms:\n"
            + "\n".join(lines)
            + "\n\nExact field-by-field details तभी final मानें जब वे indexed/allowed official source या official portal screen में दिखें।"
        )

    lines = [
        f"- {data['title']}: {data['summary']}"
        for data in DIGITAL_SEVA_CATEGORY_GUIDES_EN.values()
    ]
    return (
        "Category-wise safe guidance for Digital Seva forms:\n"
        + "\n".join(lines)
        + "\n\nTreat exact field-by-field details as final only when they appear in indexed/allowed official source data or on the official portal screen."
    )


def _digital_seva_context(language="en"):

    if language == "hi":
        return f"{DIGITAL_SEVA_SERVICES_CONTEXT_HI}\n\n{_category_summary('hi')}\n\n{_dsp_enhancement_context('Digital Seva Portal services', 'hi')}"

    return f"{DIGITAL_SEVA_SERVICES_CONTEXT}\n\n{_category_summary('en')}\n\n{_dsp_enhancement_context('Digital Seva Portal services', 'en')}"


def _matching_category(normalized, query):

    haystack = f" {normalized} {(query or '').lower()} "
    for category, terms in DIGITAL_SEVA_CATEGORY_KEYWORDS:
        if any(_term_matches(haystack, term) for term in terms):
            return category

    return ""


def _term_matches(haystack, term):

    if any(ord(char) > 127 for char in term):
        return term in haystack

    pattern = r"(?<![a-z0-9])" + re.escape(term) + r"(?![a-z0-9])"
    return bool(re.search(pattern, haystack))


def builtin_service_context(query, language="en"):

    text = (query or "").lower()
    normalized = (
        text.replace("fiill", "fill")
        .replace("fiil", "fill")
        .replace("gudeance", "guidance")
        .replace("guidence", "guidance")
        .replace("from", "form")
    )

    profile = profile_context(query, language=language)
    if profile:
        return profile

    if "pan card" in text or "pancard" in text or text.strip() == "pan" or " pan " in f" {text} " or "पैन" in text:
        if language == "hi":
            return f"{PAN_GUIDE_CONTEXT_HI}\n\n{PAN_DSP_CONTEXT_HI}"
        return f"{PAN_GUIDE_CONTEXT}\n\n{PAN_DSP_CONTEXT}"
    tax2win_terms = (
        "tax2win",
        "tax to win",
        "taxto win",
        "tax win",
        "income tax return",
        "itr filing",
        "itr form",
        "tax return",
        "tax filing",
        "income tax form",
    )
    tax2win_terms_hi = ("इनकम टैक्स", "आईटीआर", "आयकर", "टैक्स रिटर्न", "टैक्स फाइल")
    if any(term in normalized for term in tax2win_terms) or any(term in query for term in tax2win_terms_hi):
        if language == "hi":
            return f"{TAX2WIN_GUIDE_CONTEXT_HI}\n\n{TAX_DSP_CONTEXT_HI}"
        return f"{TAX2WIN_GUIDE_CONTEXT}\n\n{TAX_DSP_CONTEXT}"

    category = _matching_category(normalized, query)
    if category:
        return _category_context(category, language=language)

    digital_seva_terms = (
        "digital seva",
        "digitalseva",
        "csc service",
        "csc services",
        "csc form",
        "csc forms",
        "all form",
        "all forms",
        "fill all form",
        "fill all forms",
        "all service",
        "all services",
        "forms available",
        "portal services",
    )
    digital_seva_terms_hi = ("डिजिटल सेवा", "सीएससी", "सभी फॉर्म", "सभी सेव")
    generic_form_terms_hi = ("फॉर्म कैसे", "आठवीं", "8वीं")
    csc_scope = (
        "csc" in normalized
        or "digital seva" in normalized
        or "digitalseva" in normalized
        or "portal services" in normalized
        or "all form" in normalized
        or "all service" in normalized
        or any(term in query for term in digital_seva_terms_hi)
    )
    generic_form_intent = (
        ("fill" in normalized and "form" in normalized)
        or "filling" in normalized
        or "guidance" in normalized
        or "class 8" in normalized
        or "8th" in normalized
        or any(term in query for term in generic_form_terms_hi)
    ) and csc_scope
    if any(term in normalized for term in digital_seva_terms) or any(term in query for term in digital_seva_terms_hi) or generic_form_intent:
        return _digital_seva_context(language=language)

    return ""
