"""Resume generator that creates clean LaTeX resumes from structured data."""

from .schema import Award, Bullet, Education, Job, Leadership, Profile, Project, Resume

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
