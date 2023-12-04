from pylatex import utils, Document, Section, Command, Itemize, Head, PageStyle
from pylatex.base_classes.command import Arguments
from pylatex.basic import LineBreak
from pylatex.base_classes.containers import Environment, UserList
from pylatex.package import Package
from schema import Resume, Profile, Job, Education


def format_date_range(start_date, end_date):
    def format_date(raw_date):
        return raw_date.strftime("%b %Y")

    if end_date is None:
        end_date_str = "Present"
    else:
        end_date_str = format_date(end_date)
    start_date_str = format_date(start_date)
    return f"{start_date_str} -- {end_date_str}"


class FlushLeft(Environment):
    start_arguments = ["flushleft"]


class FlushRight(Environment):
    start_arguments = ["flushright"]


class MiniPage(Environment):
    start_arguments = ["minipage"]


class LatexVisitor:
    def __init__(self, filename):
        self.filename = filename
        self.document = Document(
            geometry_options={"margin": "1in", "top": "0.5in"}, page_numbers=False
        )

    def visitResume(self, resume: Resume):
        #     textwrap.dedent(
        #     r"""
        #     \titleformat{\section}{
        #         \vspace{-3pt}\scshape\raggedright\large
        #     }{}{0em}{}[\color{black}\titlerule \vspace{-5pt}]
        #     """
        #     )
        # ))
        self.document.packages.append(Package("enumitem"))
        self.document.packages.append(Package("titlesec"))
        # self.document.packages.append(Package("hyperref"))
        self.document.packages.append(
            Package("hyperref", options="colorlinks, urlcolor=blue")
        )
        # self.document.append(Command("setitemize", "noitemsep,topsep=0.5pt"))
        self.document.append(Command("setitemize", "noitemsep"))
        self.document.append(Command("urlstyle", "same"))
        # self.document.append(Command("titleformat*", arguments=utils.NoEscape("\section"), extra_arguments=utils.NoEscape(r"\Large\scshape")))
        # self.document.append(Command("titleformat*", utils.NoEscape("\section"), utils.NoEscape(r"\Large\scshape"), "", "", Command("rule", options="0.8pt")))
        # self.document.append(Command("titleformat",
        #                              Arguments(
        #                                 utils.NoEscape("\section"),
        #                                 utils.NoEscape(r"\Large\scshape"),
        #                                 "",
        #                                 "",
        #                                 "",
        #                                 Command("titlerule", options="0.8pt"))
        #                                 ))
        # FIXME
        self.document.append(
            utils.NoEscape(
                r"\titleformat{\section}{\Large\scshape}{\thesection}{1em}{}[{\titlerule[0.8pt]}]"
            )
        )
        # self.document.append(utils.NoEscape(r"\titlespacing*{\section}{0pt}{0\baselineskip}{\baselineskip}"))
        self.document.append(utils.NoEscape(r"\titlespacing*{\section}{0pt}{0ex}{2ex}"))
        # self.document.append(Command("titleformat", utils.NoEscape(r"\titlerule")))
        self.visitProfile(resume.profile)
        self.visitEmployment(resume.work)
        self.visitSkillsSection(resume)
        self.visitEducationSection(resume.education)
        if self.filename is None:
            print(self.document.dumps())
        else:
            self.document.generate_pdf(self.filename)

    def visitProfile(self, profile: Profile):
        with self.document.create(FlushLeft()):
            self.document.append(Command("LARGE"))
            self.document.append(utils.bold(profile.name))

        with self.document.create(MiniPage(arguments=utils.NoEscape(r"0.5\textwidth"))):
            with self.document.create(FlushLeft()):
                self.document.append(profile.phone)
                self.document.append(LineBreak())
                self.document.append(profile.email)
        with self.document.create(MiniPage(arguments=utils.NoEscape(r"0.5\textwidth"))):
            with self.document.create(FlushRight()):
                self.document.append(Command("url", utils.NoEscape(profile.linkedin)))
                self.document.append(LineBreak())
                self.document.append(Command("url", utils.NoEscape(profile.site)))
        self.document.append(LineBreak())

    def visitJob(self, job: Job):
        self.document.append(Command("noindent"))
        with self.document.create(
            MiniPage(arguments=utils.NoEscape(r"0.75\textwidth"))
        ):
            with self.document.create(FlushLeft()):
                self.document.append(utils.bold(job.title))
                self.document.append(LineBreak())
                self.document.append(utils.bold(job.employer))
        with self.document.create(
            MiniPage(arguments=utils.NoEscape(r"0.25\textwidth"))
        ):
            with self.document.create(FlushRight()):
                self.document.append(Command("raggedleft"))
                self.document.append(
                    utils.bold(
                        utils.NoEscape(format_date_range(job.start_date, job.end_date))
                    )
                )
                self.document.append(LineBreak())
                self.document.append(utils.bold(job.location))
        if len(job.description) > 0:
            with self.document.create(Itemize()) as itemize:
                for bullet in job.description:
                    itemize.add_item(bullet.content)
        else:
            self.document.append(LineBreak())
            self.document.append(LineBreak())

    def visitEmployment(self, jobs: list[Job]):
        with self.document.create(Section("Employment", numbering=False)):
            for job in jobs:
                self.visitJob(job)

    def visitEducationSection(self, education_list: list[Education]):
        with self.document.create(Section("Education", numbering=False)):
            for education in education_list:
                self.visitEducation(education)

    def visitEducation(self, education: Education):
        self.document.append(Command("noindent"))
        with self.document.create(
            MiniPage(arguments=utils.NoEscape(r"0.75\textwidth"))
        ):
            with self.document.create(FlushLeft()):
                self.document.append(utils.bold(education.degree))
                # self.document.append(LineBreak())
                self.document.append(", ")
                self.document.append(utils.italic(education.honors))
                self.document.append(", GPA: " + str(education.gpa))
                self.document.append(LineBreak())
                self.document.append(utils.bold(education.institution))
                self.document.append(LineBreak())
        self.document.append(Command("hfill"))
        with self.document.create(
            MiniPage(arguments=utils.NoEscape(r"0.25\textwidth"))
        ):
            with self.document.create(FlushRight()):
                self.document.append(Command("raggedleft"))
                self.document.append(
                    utils.NoEscape(
                        format_date_range(education.start_date, education.end_date)
                    )
                )
                self.document.append(LineBreak())
                self.document.append(education.location)
                self.document.append(LineBreak())
        self.document.append(Command("hfill"))

    def visitSkillsSection(self, resume: Resume):
        with self.document.create(Section("Skills", numbering=False)):
            self.visitLanguages(resume.languages)
            self.visitTools(resume.tools)

    def visitTools(self, tools: list[str]):
        with self.document.create(FlushLeft()):
            self.document.append(utils.bold("Tools: "))
            self.document.append(", ".join(tools))

    def visitLanguages(self, languages: list[str]):
        with self.document.create(FlushLeft()):
            self.document.append(utils.bold("Languages: "))
            self.document.append(", ".join(languages))
