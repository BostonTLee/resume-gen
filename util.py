from schema import Resume

def omit_sensitive_info(resume: Resume) -> Resume:
    if resume.profile and resume.profile.email:
        resume.profile.email = "(Email omitted)"
    if resume.profile and resume.profile.phone:
        resume.profile.phone = "(Phone omitted)"
    return resume