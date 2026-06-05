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


def builtin_service_context(query):

    text = (query or "").lower()
    if "pan card" in text or "pancard" in text or text.strip() == "pan" or " pan " in f" {text} ":
        return PAN_GUIDE_CONTEXT

    return ""
