from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
import models
from database import engine, get_db

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="NurseryConnect API", version="1.0")

@app.get("/")
def read_root():
    return {"message": "Welcome to NurseryConnect API!"}

@app.post("/children/")
def create_child(first_name: str, last_name: str, room_name: str, allergies: str = None, db: Session = Depends(get_db)):
    db_child = models.Child(first_name=first_name, last_name=last_name, room_name=room_name, allergies=allergies)
    db.add(db_child)
    db.commit()
    db.refresh(db_child)
    return {"message": "Child registered successfully", "child_id": db_child.id}

@app.get("/children/")
def get_children(db: Session = Depends(get_db)):
    children = db.query(models.Child).all()
    return children

@app.post("/incidents/")
def log_incident(child_id: int, origin: str, description: str, action_taken: str = None, db: Session = Depends(get_db)):
    db_incident = models.Incident(
        child_id=child_id,
        incident_origin=origin,
        description=description,
        action_taken=action_taken
    )
    db.add(db_incident)
    db.commit()
    db.refresh(db_incident)
    return {"message": "Incident logged successfully", "incident_id": db_incident.id}

@app.put("/incidents/{incident_id}/sign")
def sign_incident(incident_id: int, db: Session = Depends(get_db)):
    incident = db.query(models.Incident).filter(models.Incident.id == incident_id).first()
    if not incident:
        return {"error": "Incident not found"}
    incident.is_signed_by_parent = True
    db.commit()
    db.refresh(incident)
    return {"message": "Incident successfully signed by parent!", "incident_id": incident.id, "is_signed": incident.is_signed_by_parent}

@app.post("/daily-logs/")
def create_daily_log(child_id: int, log_type: str, details: str, db: Session = Depends(get_db)):
    db_log = models.DailyLog(child_id=child_id, log_type=log_type, details=details)
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return {"message": "Daily log added successfully", "log_id": db_log.id}

@app.get("/daily-logs/{child_id}")
def get_daily_logs(child_id: int, db: Session = Depends(get_db)):
    logs = db.query(models.DailyLog).filter(models.DailyLog.child_id == child_id).all()
    return {"child_id": child_id, "logs": logs}

@app.post("/medication-forms/")
def create_medication_form(child_id: int, medicine_name: str, dosage: str, time_to_give: str, parent_signature: str, db: Session = Depends(get_db)):
    db_form = models.MedicationForm(
        child_id=child_id,
        medicine_name=medicine_name,
        dosage=dosage,
        time_to_give=time_to_give,
        parent_signature=parent_signature
    )
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return {"message": "Medication form submitted and signed successfully", "form_id": db_form.id}

@app.post("/eyfs-observations/")
def create_eyfs_observation(child_id: int, area_of_learning: str, observation_text: str, photo_url: str = None, db: Session = Depends(get_db)):
    db_obs = models.EyfsObservation(
        child_id=child_id,
        area_of_learning=area_of_learning,
        observation_text=observation_text,
        photo_url=photo_url
    )
    db.add(db_obs)
    db.commit()
    db.refresh(db_obs)
    return {"message": "EYFS observation saved successfully", "observation_id": db_obs.id}

@app.post("/sleep-logs/")
def create_sleep_log(child_id: int, start_time: str, end_time: str, notes: str = None, db: Session = Depends(get_db)):
    db_sleep = models.SleepLog(child_id=child_id, start_time=start_time, end_time=end_time, notes=notes)
    db.add(db_sleep)
    db.commit()
    db.refresh(db_sleep)
    return {"message": "Sleep log recorded successfully", "sleep_id": db_sleep.id}

@app.post("/diet-milk-forms/")
def create_diet_milk_form(child_id: int, milk_type: str, amount_oz: str, dietary_requirements: str = None, db: Session = Depends(get_db)):
    db_form = models.DietAndMilkForm(
        child_id=child_id,
        milk_type=milk_type,
        amount_oz=amount_oz,
        dietary_requirements=dietary_requirements
    )
    db.add(db_form)
    db.commit()
    db.refresh(db_form)
    return {"message": "Diet and milk instructions saved successfully", "form_id": db_form.id}


@app.post("/attendance/")
def mark_attendance(child_id: int, date: str, status: str, check_in_time: str = None, check_out_time: str = None, db: Session = Depends(get_db)):
    db_att = models.Attendance(child_id=child_id, date=date, status=status, check_in_time=check_in_time, check_out_time=check_out_time)
    db.add(db_att)
    db.commit()
    db.refresh(db_att)
    return {"message": "Attendance marked successfully", "attendance_id": db_att.id}

@app.post("/key-persons/")
def assign_key_person(child_id: int, staff_name: str, room_name: str, db: Session = Depends(get_db)):
    db_kp = models.KeyPerson(child_id=child_id, staff_name=staff_name, room_name=room_name)
    db.add(db_kp)
    db.commit()
    db.refresh(db_kp)
    return {"message": "Key person assigned successfully", "assignment_id": db_kp.id}

@app.post("/emergency-contacts/")
def add_emergency_contact(child_id: int, contact_name: str, relationship: str, phone_number: str, db: Session = Depends(get_db)):
    db_ec = models.EmergencyContact(child_id=child_id, contact_name=contact_name, relationship=relationship, phone_number=phone_number)
    db.add(db_ec)
    db.commit()
    db.refresh(db_ec)
    return {"message": "Emergency contact added successfully", "contact_id": db_ec.id}

@app.post("/invoices/")
def create_invoice(child_id: int, amount_due: str, month: str, db: Session = Depends(get_db)):
    db_inv = models.Invoice(child_id=child_id, amount_due=amount_due, month=month, is_paid=False)
    db.add(db_inv)
    db.commit()
    db.refresh(db_inv)
    return {"message": "Invoice created successfully", "invoice_id": db_inv.id}


@app.post("/garden-register/")
def log_garden_register(child_id: int, time_out: str, date: str, time_in: str = None, db: Session = Depends(get_db)):
    db_item = models.GardenRegister(child_id=child_id, time_out=time_out, time_in=time_in, date=date)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"message": "Garden register logged successfully", "id": db_item.id}

@app.post("/new-joiners/")
def register_new_joiner(child_full_name: str, start_date: str, desired_sessions: str, parent_contact_email: str, db: Session = Depends(get_db)):
    db_item = models.NewJoinerRegistration(child_full_name=child_full_name, start_date=start_date, desired_sessions=desired_sessions, parent_contact_email=parent_contact_email)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"message": "New joiner application recorded", "id": db_item.id}

@app.post("/external-medications/")
def create_external_medication(person_type: str, person_name: str, medicine_details: str, dosage_and_time: str, authorized_by: str, db: Session = Depends(get_db)):
    db_item = models.ExternalMedicationForm(person_type=person_type, person_name=person_name, medicine_details=medicine_details, dosage_and_time=dosage_and_time, authorized_by=authorized_by)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"message": "Medication form saved for child or staff", "id": db_item.id}

@app.post("/health-care-plans/")
def create_health_care_plan(child_id: int, condition_name: str, symptoms_and_triggers: str, emergency_action_plan: str, db: Session = Depends(get_db)):
    db_item = models.HealthCarePlan(child_id=child_id, condition_name=condition_name, symptoms_and_triggers=symptoms_and_triggers, emergency_action_plan=emergency_action_plan)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"message": "Health care plan created successfully", "id": db_item.id}

@app.post("/staff-visitor-register/")
def log_staff_visitor(visitor_name: str, role_or_company: str, sign_in_time: str, date: str, sign_out_time: str = None, db: Session = Depends(get_db)):
    db_item = models.StaffVisitorRegister(visitor_name=visitor_name, role_or_company=role_or_company, sign_in_time=sign_in_time, sign_out_time=sign_out_time, date=date)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"message": "Visitor/Staff sign-in logged successfully", "id": db_item.id}

@app.post("/headcounts/")
def record_headcount(room_name: str, session_type: str, total_children_present: int, staff_count: int, recorded_by: str, date: str, db: Session = Depends(get_db)):
    db_item = models.Headcount(room_name=room_name, session_type=session_type, total_children_present=total_children_present, staff_count=staff_count, recorded_by=recorded_by, date=date)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return {"message": "Session headcount recorded successfully", "id": db_item.id}


@app.get("/garden-register/")
def get_garden_registers(db: Session = Depends(get_db)):
    return db.query(models.GardenRegister).all()

@app.get("/new-joiners/")
def get_new_joiners(db: Session = Depends(get_db)):
    return db.query(models.NewJoinerRegistration).all()

@app.get("/external-medications/")
def get_external_medications(db: Session = Depends(get_db)):
    return db.query(models.ExternalMedicationForm).all()

@app.get("/health-care-plans/")
def get_health_care_plans(db: Session = Depends(get_db)):
    return db.query(models.HealthCarePlan).all()

@app.get("/staff-visitor-register/")
def get_staff_visitor_registers(db: Session = Depends(get_db)):
    return db.query(models.StaffVisitorRegister).all()

@app.get("/headcounts/")
def get_headcounts(db: Session = Depends(get_db)):
    return db.query(models.Headcount).all()



