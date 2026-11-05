"""Seed the built-in metrics that ship with the application."""

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.models import MetricDefinition

BUILTIN_METRICS: tuple[dict[str, str], ...] = (
    {"name": "coding_hours", "unit": "hours"},
    {"name": "study_hours", "unit": "hours"},
    {"name": "leetcode", "unit": "problems"},
    {"name": "github_commits", "unit": "commits"},
)


def seed_builtin_metrics(session: Session) -> int:
    """Insert any missing built-in metrics and return how many were added.

    The function is idempotent so it is safe to call at startup, from a
    migration, or from a test fixture.
    """
    # SessionLocal disables autoflush, so flush pending inserts before the
    # lookup; otherwise calling this twice before a commit would duplicate.
    session.flush()

    names = [definition["name"] for definition in BUILTIN_METRICS]
    existing = set(
        session.scalars(
            select(MetricDefinition.name).where(MetricDefinition.name.in_(names))
        ).all()
    )

    created = 0
    for definition in BUILTIN_METRICS:
        if definition["name"] in existing:
            continue
        session.add(MetricDefinition(is_builtin=True, **definition))
        created += 1

    session.flush()
    return created


def main() -> None:
    """Seed a configured database from the command line."""
    from app.db.session import SessionLocal

    with SessionLocal() as session:
        created = seed_builtin_metrics(session)
        session.commit()

    print(f"Seeded {created} built-in metric(s).")


if __name__ == "__main__":
    main()
