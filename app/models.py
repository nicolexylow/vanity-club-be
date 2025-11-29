from sqlalchemy import Column, Integer, String
from .database import Base
from sqlalchemy import (
    Column,
    String,
    Date,
    DateTime,
    Time,
    Integer,
    BigInteger,
    ForeignKey,
    Numeric,
    Text,
    func,
    text,
    Table,
)
from sqlalchemy.orm import relationship
from sqlalchemy.dialects.postgresql import UUID, ARRAY, JSONB

# ---------------------------------------------------------------------------
# Association tables
# ---------------------------------------------------------------------------

# Booking <-> Service (many-to-many)
booking_services = Table(
    "booking_services",
    Base.metadata,
    Column(
        "booking_id", UUID(as_uuid=True), ForeignKey("bookings.id"), primary_key=True
    ),
    Column(
        "service_id", UUID(as_uuid=True), ForeignKey("services.id"), primary_key=True
    ),
)

# ---------------------------------------------------------------------------
# Core tables
# ---------------------------------------------------------------------------


class Address(Base):
    __tablename__ = "addresses"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    street_line_1 = Column(String, nullable=False)
    street_line_2 = Column(String, nullable=True)
    suburb = Column(String, nullable=True)
    city = Column(String, nullable=True)
    state = Column(String, nullable=True)
    postcode = Column(String, nullable=True)
    country = Column(String, nullable=True)

    latitude = Column(Numeric(9, 6), nullable=True)
    longitude = Column(Numeric(9, 6), nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # relationships
    users = relationship("User", back_populates="address")
    businesses = relationship("Business", back_populates="address")


class User(Base):
    __tablename__ = "users"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=True)
    email = Column(String, nullable=False, unique=True)
    phone = Column(String, nullable=True)
    avatar = Column(String, nullable=True)

    address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # relationships
    address = relationship("Address", back_populates="users")
    bookings = relationship("Booking", back_populates="user")


class Business(Base):
    __tablename__ = "businesses"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    email = Column(String, nullable=True)
    website = Column(String, nullable=True)
    social_media = Column(JSONB, nullable=True)
    
    address_id = Column(UUID(as_uuid=True), ForeignKey("addresses.id"), nullable=True)

    description = Column(Text, nullable=True)
    logo = Column(String, nullable=True)
    images = Column(ARRAY(String), nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # relationships
    address = relationship("Address", back_populates="businesses")
    opening_hours = relationship("OpeningHour", back_populates="business")
    bookings = relationship("Booking", back_populates="business")
    staffs = relationship("Staff", back_populates="business")
    service_categories = relationship("ServiceCategory", back_populates="business")


class Staff(Base):
    __tablename__ = "staff"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    # drawn as str[] in the diagram – store as array of strings
    position = Column(ARRAY(String), nullable=True)
    description = Column(Text, nullable=True)

    business_id = Column(
        UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False
    )

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # relationships
    business = relationship("Business", back_populates="staffs")
    qualifications = relationship("Qualification", back_populates="staff")


class Qualification(Base):
    __tablename__ = "qualifications"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    name = Column(String, nullable=False)
    company = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    certificate_id = Column(String, nullable=True)
    certificate_image = Column(ARRAY(String), nullable=True)

    staff_id = Column(UUID(as_uuid=True), ForeignKey("staff.id"), nullable=False)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # relationships
    staff = relationship("Staff", back_populates="qualifications")


class OpeningHour(Base):
    __tablename__ = "opening_hours"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    business_id = Column(
        UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False
    )

    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # relationships
    business = relationship("Business", back_populates="opening_hours")


class ServiceCategory(Base):
    __tablename__ = "service_categories"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    images = Column(ARRAY(String), nullable=True)

    # derived fields in the diagram: store as simple columns
    price_from = Column(Integer, nullable=True)
    duration_range = Column(String, nullable=True)

    business_id = Column(
        UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False
    )

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # relationships
    business = relationship("Business", back_populates="service_categories")
    services = relationship("Service", back_populates="category")


class Service(Base):
    __tablename__ = "services"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    name = Column(String, nullable=False)
    duration_mins = Column(Integer, nullable=False)
    price = Column(Integer, nullable=False)
    description = Column(Text, nullable=True)
    images = Column(ARRAY(String), nullable=True)

    service_category_id = Column(
        UUID(as_uuid=True), ForeignKey("service_categories.id"), nullable=False
    )

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # relationships
    category = relationship("ServiceCategory", back_populates="services")
    bookings = relationship(
        "Booking",
        secondary=booking_services,
        back_populates="services",
    )


class Booking(Base):
    __tablename__ = "bookings"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    # human-friendly running number
    booking_id = Column(BigInteger, autoincrement=True, unique=True, index=True)

    time = Column(DateTime(timezone=True), nullable=False)

    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    business_id = Column(
        UUID(as_uuid=True), ForeignKey("businesses.id"), nullable=False
    )

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # relationships
    user = relationship("User", back_populates="bookings")
    business = relationship("Business", back_populates="bookings")
    services = relationship(
        "Service",
        secondary=booking_services,
        back_populates="bookings",
    )
    rating = relationship("Rating", back_populates="booking", uselist=False)


class Rating(Base):
    __tablename__ = "ratings"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        server_default=text("gen_random_uuid()"),
    )

    booking_id = Column(
        UUID(as_uuid=True),
        ForeignKey("bookings.id"),
        nullable=False,
        unique=True,  # one rating per booking
    )

    stars = Column(Numeric(3, 2), nullable=False)
    description = Column(Text, nullable=True)

    created_at = Column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    # relationships
    booking = relationship("Booking", back_populates="rating")
