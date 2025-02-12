"""Resume generator that creates clean LaTeX resumes from structured data."""

from .schema import Resume, Profile, Job, Education, Leadership, Project, Award, Bullet

__version__ = "0.1.0"
__all__ = [
    "Resume",
    "Profile",
    "Job",
    "Education",
    "Leadership",
    "Project",
    "Award",
    "Bullet",
]
