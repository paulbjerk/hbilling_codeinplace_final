"""
This program aims to create a simple interface linking
health care providers (clinics),
health insurance providers (insurers)
and patients(insured).

Any patient name and ID number can be entered,
but images of Fred Flintstone, Wilma Flintstone, Barney Rubble, and Betty Rubble are registered
in the system with ID photos.

The program tracks their clinic visits
by procedure and its associated costs.
For the sake of simplicity in development
the program uses internal lists and dictionaries
rather than external csv and json files,
but external files would be substituted in a full deployment.
Right now it only has a workflow that moves a patient through
a single clinic and insurer, and really only works if the
initial patient is brought through the whole process before
another patient is entered.

User inputs
    Define User: Patient, Receptionist, Clinician, Insurer, Auditor
    Define Activity: Data entry, Query, Audit, Payment
    Activity Entries: Prompts user for inputs that initiate activity

Clinician Role and Activity:
The clinician represents a clinic as a whole, doctors and staff
who provide services to patients. Clinicians enter data related to
patient identity, medical conditions, and medical services. Clinicians
receive payments from insurers for services rendered. Clinics can
add new patients. A patient who is not included in the insured patient
database is considered uninsured and that patient's insurer will return
as None.

Patient Role and Activity:
The patient is an individual identified by a patient identification
number (pid) who presents medical conditions at the clinic and receives
medical services from the clinic. A patient has only one
insurer, but may visit more than one clinic. A patient has two
parallel identies that both should have the same values that
can be verified against each other, as patient (pid) and insured (iid),
which are the same identifying names and id number as a key value. A
patient tranisitions into an insured after being treated in a clinic.

Insurer Role and Activity:
The insurer is a company that provides payments to clinics
based on medical services provided according to contracted
prices per medical services as presented in standardized
medical codes. An insurer can maintain different contracts
with different clinics with different payment rates for the
same services at different clinics. For the sake of the program
patients are all accorded insurance, with the exception of
uninsured patients whose insurance returns None.

Auditor Role and Activity:
The auditor is a back-office that both encodes medical services
according to standardized medical codes, and in the process
provides an auditing function that seeks consensus between
the clinic and insurers about what services will be compensated
with payments to the clinic.

For the sake of this program, all four of these users have access
to full patient and clinic records, but in real-life there
would be data restrictions that would limit information to
relevant users only for each patient, clinic, and insurer.


Record Updates and Resolution
The Auditory role is the last user activity step.
Once the auditor enters a medical service code that
accords with a medical diagnostic code, then
the program automatically updates all relevant records.
The program resolves when all services have been coded
and audited, which prompts the program to calculate payment and
withdraw money from the relevant insurer account
and deposit an equivalent amount to the relevant
clinic accounts.

"""

from simpleimage import SimpleImage

INS1 = "BlueCross BlueShield"
INS2 = "ACA"
INS3 = "Medicaid"

CLC1 = "University Medical Centre"
CLC2 = "Covenant Hospital"
CLC3 = "Quaker Urgent Care Clinic"

# insured_list = ["19700101", "19710101"]


# "19710101": ["19710101", "Paul", "Bjerk", "foot hurts", "0000"]
INITIAL_CLINIC_BALANCE = float(0)
PAYMENT_CODES = {"1111": int(1001), "2222": int(2002), "3333": int(3033), "4444": int(4404)}
MEDICAL_CODES = {"1111": "foot treatment", "2222": "hand treatment", "3333": "head treatment",
                 "4444": "whole body treatment"}


# "19720101": "Wilma Flintstone", "19700101": "Fred Flintstone", "19710101": "Barney Rubble"

def main():
    # mutable data sets
    waiting_room = []
    patients_for_processing = []
    patients_in_treatment = []
    insured_for_auditing = []
    invoices_for_payment = {}
    payment_register = []
    current_balance = int(0)

    # there is a problem with the repopulation of the waiting room
    # user input
    resolved = "working"
    starting_data = ["Enter New Patient", "To Enter New Patient", "Press 1", "PatientEntryNeeded", "PatientEntryNeeded"]

    # user = "NewEntry"
    while resolved == "working":
        user = initial_role_entry("NewEntry")
        user_role = str(user)
        data_input = role_entry(user, starting_data)
        if user_role == "1":
            waiting_room.append(data_input)
            # waiting_room[str(data_input[0])] = data_input
            if len(waiting_room) > 0:
                starting_data = waiting_room[0]
            else:
                starting_data = ["Enter New Patient", "To Enter New Patient", "Press 1", "PatientEntryNeeded",
                                 "PatientEntryNeeded"]
            print("These patients are in the waiting room: ")
            for i in range(len(waiting_room)):
                print(str(waiting_room[i]))
        elif user_role == "2":
            # del waiting_room[str(data_input[0])]
            patients_for_processing.append(data_input)
            waiting_room.pop(0)
            # starting_data = patients_for_processing[0]
            # another_entry = input("Do you want to register the next patient? Type y or n : ")
            # if another_entry == "y":
            # print("Type 2 to register the next patient")
            if len(waiting_room) > 0:
                starting_data = waiting_room[0]
            # elif len(waiting_room) == 0:
            # starting_data = ["Enter New Patient", "To Enter New Patient", "Press 1", "PatientEntryNeeded", "PatientEntryNeeded"]
            else:
                starting_data = patients_for_processing[0]
            # patients_for_processing[str(data_input[0])] = data_input
            # if len(patients_for_processing) > 0:
            # starting_data = patients_for_processing[0]
            # else:
            # starting_data = ["Enter New Patient", "To Enter New Patient", "Press 1", "PatientEntryNeeded", "PatientEntryNeeded"]

            print("These patients are in the waiting room: ")
            for i in range(len(waiting_room)):
                print(str(waiting_room[i]))
            print("These patients have been sent to treatment: ")
            for i in range(len(patients_for_processing)):
                print(str(patients_for_processing[i]))
            # starting_data = patients_for_processing[0]

        elif user_role == "3":
            patients_in_treatment.append(data_input)
            patients_for_processing.pop(0)
            # starting_data = patients_for_processing[0]
            if len(patients_for_processing) > 0:
                starting_data = patients_for_processing[0]
            # elif len(patients_for_processing) < 1:
            # starting_data = ["Enter New Patient", "Receptionist Enter New Patient", "Press 2", "PatientEntryNeeded", "PatientEntryNeeded"]
            else:
                starting_data = patients_in_treatment[0]
            # patients_for_processing.pop(0)
            print("These patients are in the waiting room: ")
            for i in range(len(waiting_room)):
                print(str(waiting_room[i]))
            print("These patients have been sent to treatment: ")
            for i in range(len(patients_for_processing)):
                print(str(patients_for_processing[i]))
            print("These patients have been treated: ")
            for i in range(len(patients_in_treatment)):
                print(str(patients_in_treatment[i]))
            # starting_data = patients_in_treatment[0]
        elif user_role == "4":
            insured_for_auditing.append(data_input)
            patients_in_treatment.pop(0)
            if len(patients_in_treatment) > 0:
                starting_data = patients_in_treatment[0]
            # elif len(patients_in_treatment) < 1:
            # starting_data = ["Enter New Patient", "Clinician Enter New Patient", "Press 3", "PatientEntryNeeded", "PatientEntryNeeded"]
            else:
                starting_data = insured_for_auditing[0]

            print("These insured have been processed: ")
            for i in range(len(insured_for_auditing)):
                print(str(insured_for_auditing[i]))
            # starting_data = insured_for_auditing[0]
        elif user_role == "5":

            # for elem in range (len(insured_for_auditing)):
            invoices_for_payment[str(insured_for_auditing[0][0])] = insured_for_auditing[0][4]
            print("These insured have been processed: ")
            for i in range(len(insured_for_auditing)):
                print(str(insured_for_auditing[i]))
            print("These cases are ready for invoicing and payment: ")
            for key in invoices_for_payment:
                print(str(invoices_for_payment[key]))
            insured_for_auditing.pop(0)
            if len(insured_for_auditing) > 0:
                starting_data = insured_for_auditing[0]
            # elif len(insured_for_auditing) < 1:
            # starting_data = ["Enter New Patient", "Insurer Enter New Patient", "Press 4", "PatientEntryNeeded", "PatientEntryNeeded"]
            else:
                starting_data = data_input

            for key in invoices_for_payment:
                current_balance += process_payment(invoices_for_payment[key])
                print("The new clinic balance is: $" + str(current_balance))
            # print("These patients are in the waiting room: " + str(waiting_room))
            # print("These patients have been sent to treatment: " + str(patients_for_processing))
            # print("These patients have been treated: " + str(patients_in_treatment))
            invoices_for_payment.clear()
            print("These patients are in the waiting room: ")
            for i in range(len(waiting_room)):
                print(str(waiting_room[i]))
            print("These patients have been sent to treatment: ")
            for i in range(len(patients_for_processing)):
                print(str(patients_for_processing[i]))
            print("These patients have been treated: ")
            for i in range(len(patients_in_treatment)):
                print(str(patients_in_treatment[i]))
            print("These insured have been processed: ")
            for i in range(len(insured_for_auditing)):
                print(str(insured_for_auditing[i]))
        # starting_data = data_input


def initial_role_entry(initial_user):
    user = initial_user
    user = input(
        "Please enter your user role \n 1 for Patient \n 2 for Receptionist \n 3 for Clinician \n 4 for Insurer \n 5 for Auditor \n Type exit to exit the program \n Entry: ")
    if user == "1" or user == "2" or user == "3" or user == "4" or user == "5" or user == "exit":
        return user
    else:
        main()
        # role_entry(1, ["Enter New Patient", "To Enter New Patient", "Press 1", "PatientEntryNeeded", "PatientEntryNeeded"])
        # user = input("Please re-enter your user role (1, 2, 3, 4, or 5) \n 1 for Clinician \n 2 for Patient \n 3 for Insurer \n 4 for Auditor \n or type exit to exit \n Entry: ")
    # user = user_attempt
    # print(user)

    # return user


def role_entry(user, starting_data):
    # if user != "1" or "2" or "3" or "4" or "5" or "exit":
    # input("Please re-enter your user role (1, 2, 3, or 4) \n 1 for Clinician \n 2 for Patient \n 3 for Insurer \n 4 for Coder \n or type exit to exit \n Entry: ")
    if user == "1":
        padmit_sheet = patient_entry()
        return padmit_sheet
    elif user == "2":
        cadmit_sheet = reception_entry(starting_data)
        return cadmit_sheet
    elif user == "3":
        ctreatment_sheet = clinic_entry(starting_data)
        return ctreatment_sheet
    elif user == "4":
        ins_treatment_sheet = insurer_entry(starting_data)
        return ins_treatment_sheet
    elif user == "5":
        audited_service = auditor_entry(starting_data)
        return audited_service
    else:
        user == "exit"
        exit()


def patient_entry():
    pfirstname = input("Please enter your first name (or type EXIT to start over): ")
    pfirstname = pfirstname.strip()
    accidental_full = pfirstname.split(" ")
    pfirstname = str(accidental_full[0])
    if pfirstname == "EXIT":
        main()
        # initial_role_entry("NewEntry")
        # role_entry("1", ["Enter New Patient", "To Enter New Patient", "Press 1", "PatientEntryNeeded", "PatientEntryNeeded"])
    pfirstname = pfirstname.lower()
    plastname = input("Please enter your last name: ")
    plastname = plastname.strip()
    plastname = plastname.lower()
    pid = input("Please enter your patient identification number: ")
    pcomplaint = input("Please explain your symptoms or reason for this visit: ")
    pcode = "xxxx"
    # print("Medical staff will enter a code here for you")
    padmit_sheet = [pid, pfirstname, plastname, pcomplaint, pcode]
    return padmit_sheet


def reception_entry(padmit_sheet):
    pid = padmit_sheet[0]
    plastname = padmit_sheet[2]
    cid = input("To enter new patient information, press 1, or press enter to continue: ")
    if cid == "1":
        main()
    else:
        cadmit_sheet = padmit_sheet
        cadmit_sheet[0] = "NoEntry"
        print("Please confirm identity and enter the identification number for: " + str(cadmit_sheet[1]) + " " + str(
            cadmit_sheet[2]))
        show_photo = input("Press p to view the photo: ")
        if show_photo == "p":
            image = "images/" + str(padmit_sheet[1]) + str(padmit_sheet[2]) + ".jpg"
        if str(image) == "images/fredflintstone.jpg":
            photo = SimpleImage(image)
            photo.show()
        elif str(image) == "images/wilmaflintstone.jpg":
            photo = SimpleImage(image)
            photo.show()
        elif str(image) == "images/barneyrubble.jpg":
            photo = SimpleImage(image)
            photo.show()
        elif str(image) == "images/bettyrubble.jpg":
            photo = SimpleImage(image)
            photo.show()
        else:
            print("No photo available.")
    different_patient = input("If this is not the patient you are treating, type 'diff' here, otherwise press Enter: ")
    if different_patient == "diff":
        pfirstname = input("Please enter patient's first name: ")
        pfirstname = pfirstname.strip()
        accidental_full = pfirstname.split(" ")
        pfirstname = str(accidental_full[0])
        # initial_role_entry("NewEntry")
        # role_entry("1", ["Enter New Patient", "To Enter New Patient", "Press 1", "PatientEntryNeeded", "PatientEntryNeeded"])
        pfirstname = pfirstname.lower()
        plastname = input("Please enter patient's last name: ")
        plastname = plastname.strip()
        plastname = plastname.lower()
        pid = input("Please enter the new patient's identification number: ")
        pcomplaint = input("Please detail the patient's symptoms: ")
        pcode = "xxxx"
        cadmit_sheet = [pid, pfirstname, plastname, pcomplaint, pcode]
    different_patient = "done"
    cid = input("Please confirm patient's ID number: ")
    cadmit_sheet[0] = cid
    cid = cadmit_sheet[0]
    clastname = cadmit_sheet[2]
    if (str(pid) + str(plastname)) != (str(cid) + str(clastname)):
        cid = input("ID number does not match. Please re-enter patient ID number: ")
        cadmit_sheet[0] = cid
    else:
        cadmit_sheet[0] = cid
    ccomplaint = input("Please give details about the patient's stated symptoms: ")
    cadmit_sheet[3] = ccomplaint
    ccode = input("Please enter relevant medical code (type 0000 if unknown): ")
    cadmit_sheet[4] = ccode

    print("This patient has been sent to treatment: " + str(cadmit_sheet))
    # cadmit_sheet = [cid, cfirstname, clastname, ccomplaint, ccode]
    return cadmit_sheet


def clinic_entry(cadmit_sheet):
    ctreatment_sheet = cadmit_sheet
    print(str(ctreatment_sheet[1]) + " " + str(ctreatment_sheet[2]) + " complained of " + str(ctreatment_sheet[3]))
    different_patient = input("If this is not the patient you are treating, type 'diff' here, otherwise press Enter: ")
    if different_patient == "diff":
        pfirstname = input("Please enter patient's first name: ")
        pfirstname = pfirstname.strip()
        accidental_full = pfirstname.split(" ")
        pfirstname = str(accidental_full[0])
        # initial_role_entry("NewEntry")
        # role_entry("1", ["Enter New Patient", "To Enter New Patient", "Press 1", "PatientEntryNeeded", "PatientEntryNeeded"])
        pfirstname = pfirstname.lower()
        plastname = input("Please enter patient's last name: ")
        plastname = plastname.strip()
        plastname = plastname.lower()
        pid = input("Please enter the patient's identification number: ")
        pcomplaint = input("Please detail your treatment of the patient: ")
        pcode = "xxxx"
        ctreatment_sheet = [pid, pfirstname, plastname, pcomplaint, pcode]
    different_patient = "done"
    # print("Medical staff will enter a code here for you")
    # padmit_sheet = [pid, pfirstname, plastname, pcomplaint, pcode]

    print("Enter proposed medical code below.")
    get_help = input("For help with codes, press h or press Enter to continue: ")
    if get_help == "h":
        print(MEDICAL_CODES)
    ccode = input("Please enter relevant medical code: ")
    if ccode == "":
        # while (str(ccode) is not "1111") or (str(ccode) is not "2222") or (str(ccode) is not "3333") or (str(ccode) is not "4444"):
        ccode = input("A code must be entered here. Please enter relevant medical code: ")

    # for key in MEDICAL_CODES:
    # if ccode != MEDICAL_CODES[key]:
    # get_help = input("For help with codes, press h or press Enter to continue: ")
    # if get_help == "h":
    # print(MEDICAL_CODES)
    # ccode = input("A code must be entered here. Please enter relevant medical code: ")

    ctreatment_sheet[4] = ccode
    return ctreatment_sheet


def insurer_entry(ctreatment_sheet):
    ins_treatment_sheet = ctreatment_sheet
    print("The patient was treated for " + str(ctreatment_sheet[3]))
    print("The treatment given was coded by the clinic as: " + str(ctreatment_sheet[4]))
    help = input("For help with codes, press h, to continue press Enter: ")
    if help == "h":
        print(MEDICAL_CODES)
    ins_code = input("Is the given medical code correct? If so, please re-type it here, or type the correct code: ")
    if ins_code == str(ctreatment_sheet[4]):
        ins_treatment_sheet = ctreatment_sheet
    else:
        ins_treatment_sheet[4] = str(ins_code)
    return ins_treatment_sheet


def auditor_entry(ins_treatment_sheet):
    auditor_sheet = ins_treatment_sheet
    print("The patient was treated for " + str(ins_treatment_sheet[3]))
    print("The treatment given was coded by the INSURER as: " + str(ins_treatment_sheet[4]))
    get_help = input("For help with codes, press h or press Enter to continue: ")
    if get_help == "h":
        print(MEDICAL_CODES)
    auditor_code_1 = input("Please type the correct medical code here: ")
    auditor_code_2 = input("Double check: Please re-enter the correct medical code here: ")
    if auditor_code_1 == auditor_code_2:
        auditor_sheet[4] = auditor_code_2
    else:
        auditor_code_3 = input("Double check: Please re-enter the correct medical code here: ")
        auditor_sheet[4] = auditor_code_3
    return auditor_sheet


def process_payment(service_code):
    print("Service Code " + str(service_code) + " is billed at $" + str(PAYMENT_CODES[service_code]))
    payment_amount = float(PAYMENT_CODES[service_code])
    return payment_amount


def make_payments(payment_register):
    next_payment = "yes"
    return next_payment


def add_insured():
    ifirstname = input("Please enter the insured's first name: ")
    ilastname = input("Please enter the insured's last name: ")
    iid = input("Please enter the insured's identification number: ")
    icomplaint = input("Please enter the insured's sytomps: ")
    icode = input("Please enter the relevant medical code: ")
    insured = [iid, ifirstname, ilastname, icomplaint, icode]
    return insured


if __name__ == '__main__':
    main()
