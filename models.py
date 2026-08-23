from datetime import datetime
from sqlalchemy import Column, Integer, String, Text, Boolean, DateTime, ForeignKey
from database import Base

class Child(Base):
    __tablename__ = "children"
    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    room_name = Column(String)
    allergies = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class Incident(Base):
    __tablename__ = "incidents"
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    incident_origin = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    action_taken = Column(Text)
    is_signed_by_parent = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class DailyLog(Base):
    __tablename__ = "daily_logs"
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    log_type = Column(String, nullable=False)
    details = Column(Text, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class MedicationForm(Base):
    __tablename__ = "medication_forms"
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    medicine_name = Column(String, nullable=False)
    dosage = Column(String, nullable=False)
    time_to_give = Column(String, nullable=False)
    parent_signature = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)

class EyfsObservation(Base):
    __tablename__ = "eyfs_observations"
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    area_of_learning = Column(String, nullable=False)
    observation_text = Column(Text, nullable=False)
    photo_url = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)


class SleepLog(Base):
    __tablename__ = "sleep_logs"
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    start_time = Column(String, nullable=False)
    end_time = Column(String, nullable=False)
    notes = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)

class DietAndMilkForm(Base):
    __tablename__ = "diet_milk_forms"
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    milk_type = Column(String, nullable=False) # e.g., 'Formula brand X' or 'Breast milk'
    amount_oz = Column(String, nullable=False) # e.g., '6 oz'
    dietary_requirements = Column(Text)
    created_at = Column(DateTime, default=datetime.utcnow)


class Attendance(Base):
    __tablename__ = "attendance"
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    date = Column(String, nullable=False)
    status = Column(String, nullable=False) # e.g., 'Present', 'Absent', 'Late'
    check_in_time = Column(String)
    check_out_time = Column(String)

class KeyPerson(Base):
    __tablename__ = "key_persons"
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    staff_name = Column(String, nullable=False)
    room_name = Column(String, nullable=False)

class EmergencyContact(Base):
    __tablename__ = "emergency_contacts"
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    contact_name = Column(String, nullable=False)
    relationship = Column(String, nullable=False) # e.g., 'Grandmother', 'Uncle'
    phone_number = Column(String, nullable=False)

class Invoice(Base):
    __tablename__ = "invoices"
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    amount_due = Column(String, nullable=False)
    month = Column(String, nullable=False) # e.g., 'September 2026'
    is_paid = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)


class GardenRegister(Base):
    __tablename__ = "garden_registers"
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    time_out = Column(String, nullable=False)
    time_in = Column(String)
    date = Column(String, nullable=False)

class NewJoinerRegistration(Base):
    __tablename__ = "new_joiners"
    id = Column(Integer, primary_key=True, index=True)
    child_full_name = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    desired_sessions = Column(String, nullable=False) # e.g., 'Full time', 'Mon-Wed'
    parent_contact_email = Column(String, nullable=False)

class ExternalMedicationForm(Base):
    __tablename__ = "external_medications"
    id = Column(Integer, primary_key=True, index=True)
    person_type = Column(String, nullable=False) # 'Child' or 'Staff'
    person_name = Column(String, nullable=False)
    medicine_details = Column(Text, nullable=False)
    dosage_and_time = Column(String, nullable=False)
    authorized_by = Column(String, nullable=False) # Parent signature or Manager signature
    created_at = Column(DateTime, default=datetime.utcnow)

class HealthCarePlan(Base):
    __tablename__ = "health_care_plans"
    id = Column(Integer, primary_key=True, index=True)
    child_id = Column(Integer, ForeignKey("children.id"), nullable=False)
    condition_name = Column(String, nullable=False) # e.g., 'Asthma', 'Severe Nut Allergy'
    symptoms_and_triggers = Column(Text, nullable=False)
    emergency_action_plan = Column(Text, nullable=False)

class StaffVisitorRegister(Base):
    __tablename__ = "staff_visitor_registers"
    id = Column(Integer, primary_key=True, index=True)
    visitor_name = Column(String, nullable=False)
    role_or_company = Column(String, nullable=False) # e.g., 'Ofsted Inspector', 'Agency Staff'
    sign_in_time = Column(String, nullable=False)
    sign_out_time = Column(String)
    date = Column(String, nullable=False)

class Headcount(Base):
    __tablename__ = "headcounts"
    id = Column(Integer, primary_key=True, index=True)
    room_name = Column(String, nullable=False)
    session_type = Column(String, nullable=False) # 'Morning Session' or 'Afternoon Session'
    total_children_present = Column(Integer, nullable=False)
    staff_count = Column(Integer, nullable=False)
    recorded_by = Column(String, nullable=False) # Staff member name
    date = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)


