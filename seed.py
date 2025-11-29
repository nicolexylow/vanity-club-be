import os
from datetime import datetime, date, time
from decimal import Decimal
from app.database import SessionLocal
from app.models import (
    Address,
    Business,
    OpeningHour,
    Staff,
    Qualification,
    ServiceCategory,
    Service,
    User,
    Booking,
    Rating,
)

DATABASE_URL = os.getenv("DATABASE_URL")

def seed():
    session = SessionLocal()

    try:
        # ------------------------------------------------------------------
        # Addresses
        # ------------------------------------------------------------------
        addr_business = Address(
            street_line_1="123 Beauty Lane",
            suburb="Surry Hills",
            city="Sydney",
            state="NSW",
            postcode="2010",
            country="Australia",
            latitude=Decimal("-33.8840"),
            longitude=Decimal("151.2120"),
        )

        addr_user = Address(
            street_line_1="45 User St",
            suburb="Newtown",
            city="Sydney",
            state="NSW",
            postcode="2042",
            country="Australia",
            latitude=Decimal("-33.8970"),
            longitude=Decimal("151.1780"),
        )

        session.add_all([addr_business, addr_user])

        # ------------------------------------------------------------------
        # Business
        # ------------------------------------------------------------------
        business = Business(
            address=addr_business,
            description="A cosy beauty studio specialising in brows, lashes, and skin treatments.",
            images=[
                "business-images/vanityclub_front.jpg",
                "business-images/vanityclub_room.jpg",
            ],
        )
        session.add(business)

        # ------------------------------------------------------------------
        # Opening Hours
        # ------------------------------------------------------------------
        opening_hours = [
            OpeningHour(
                business=business,
                date=date(2025, 12, 1),
                start_time=time(9, 0),
                end_time=time(17, 0),
            ),
            OpeningHour(
                business=business,
                date=date(2025, 12, 2),
                start_time=time(11, 0),
                end_time=time(19, 0),
            ),
        ]
        session.add_all(opening_hours)

        # ------------------------------------------------------------------
        # Staff & Qualifications
        # ------------------------------------------------------------------
        staff_1 = Staff(
            first_name="Mia",
            last_name="Chan",
            position=["Senior Brow Artist", "Lash Tech"],
            description="Specialises in natural-looking brows and lash lifts.",
            business=business,  
        )

        staff_2 = Staff(
            first_name="Olivia",
            last_name="Nguyen",
            position=["Skin Therapist"],
            description="Focuses on facials and skin health treatments.",
            business=business,
        )

        session.add_all([staff_1, staff_2])
        session.flush()  # ensure staff IDs are available

        qual_1 = Qualification(
            name="Certificate in Brow Design",
            company="Beauty Institute Sydney",
            description="Advanced techniques in brow mapping and tinting.",
            certificate_id="BROW-2022-001",
            certificate_image=["certificates/mia_brow_cert.jpg"],
            staff_id=staff_1.id,
        )

        qual_2 = Qualification(
            name="Diploma of Beauty Therapy",
            company="Skin Academy Australia",
            description="Comprehensive training in skin treatments and facials.",
            certificate_id="SKIN-2021-014",
            certificate_image=["certificates/olivia_skin_diploma.jpg"],
            staff_id=staff_2.id,
        )

        session.add_all([qual_1, qual_2])

        # ------------------------------------------------------------------
        # Service Categories
        # ------------------------------------------------------------------
        brows_category = ServiceCategory(
            name="Brows",
            description="Brow shaping, tinting and lamination services.",
            images=["service-categories/brows.jpg"],
            price_from=60,
            duration_range="30–75 mins",
            business_id=business.id,
        )

        lashes_category = ServiceCategory(
            name="Lashes",
            description="Lash lifts and tints for a natural, lifted look.",
            images=["service-categories/lashes.jpg"],
            price_from=80,
            duration_range="45–90 mins",
            business_id=business.id,
        )

        facials_category = ServiceCategory(
            name="Facials",
            description="Skin treatments tailored to your skin type.",
            images=["service-categories/facials.jpg"],
            price_from=100,
            duration_range="60–90 mins",
            business_id=business.id,
        )

        session.add_all([brows_category, lashes_category, facials_category])
        session.flush()

        # ------------------------------------------------------------------
        # Services
        # ------------------------------------------------------------------
        brow_shape_tint = Service(
            name="Brow Shape & Tint",
            duration_mins=45,
            price=70,
            description="Custom brow shaping with tint to define your brows.",
            images=["services/brow_shape_tint.jpg"],
            service_category_id=brows_category.id,
        )

        brow_lamination = Service(
            name="Brow Lamination",
            duration_mins=75,
            price=110,
            description="Full brow lamination including shape and tint.",
            images=["services/brow_lamination.jpg"],
            service_category_id=brows_category.id,
        )

        lash_lift = Service(
            name="Lash Lift",
            duration_mins=60,
            price=95,
            description="Natural lash lift to enhance your lashes without extensions.",
            images=["services/lash_lift.jpg"],
            service_category_id=lashes_category.id,
        )

        signature_facial = Service(
            name="Signature Glow Facial",
            duration_mins=75,
            price=130,
            description="Deep cleansing, exfoliation and hydration for glowing skin.",
            images=["services/signature_facial.jpg"],
            service_category_id=facials_category.id,
        )

        session.add_all([brow_shape_tint, brow_lamination, lash_lift, signature_facial])

        # ------------------------------------------------------------------
        # Users
        # ------------------------------------------------------------------
        user_1 = User(
            first_name="Nicole",
            last_name="Low",
            email="nicole@example.com",
            phone="+61 400 000 001",
            avatar="users/nicole_avatar.jpg",
            address=addr_user,
        )

        user_2 = User(
            first_name="Emily",
            last_name="Wong",
            email="emily@example.com",
            phone="+61 400 000 002",
            avatar="users/emily_avatar.jpg",
            address=None,
        )

        session.add_all([user_1, user_2])

        # ------------------------------------------------------------------
        # Bookings (with many-to-many Services)
        # ------------------------------------------------------------------
        booking_1 = Booking(
            time=datetime(2025, 12, 1, 10, 0),
            user=user_1,
            business=business,
        )

        booking_1.services = [brow_shape_tint, lash_lift]

        booking_2 = Booking(
            time=datetime(2025, 12, 2, 13, 30),
            user=user_2,
            business=business,
        )

        booking_2.services = [signature_facial]

        session.add_all([booking_1, booking_2])
        session.flush()  # to get booking IDs for ratings

        # ------------------------------------------------------------------
        # Ratings (one per booking)
        # ------------------------------------------------------------------
        rating_1 = Rating(
            booking_id=booking_1.id,
            stars=Decimal("4.8"),
            description="Loved my brows and lashes! Will definitely come back.",
        )

        rating_2 = Rating(
            booking_id=booking_2.id,
            stars=Decimal("5.0"),
            description="Skin feels amazing, very relaxing experience.",
        )

        session.add_all([rating_1, rating_2])

        # ------------------------------------------------------------------
        # Commit all changes
        # ------------------------------------------------------------------
        session.commit()
        print("✅ Seed data inserted successfully.")

    except Exception as e:
        session.rollback()
        print("❌ Error while seeding:", e)
        raise
    finally:
        session.close()


if __name__ == "__main__":
    seed()
