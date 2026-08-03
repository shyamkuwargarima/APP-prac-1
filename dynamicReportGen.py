"""
=====================================================================
 DYNAMIC REPORT GENERATOR
 Demonstrates: Decorators | classmethod | Magic (dunder) methods
=====================================================================

Author : Practical Lab Demo

Purpose : Allow a user to define report templates and apply
          formatting options (bold, uppercase, bordered, logged)
          dynamically using Python decorators, alternate
          constructors (classmethod) and operator/behaviour
          overloading (magic methods).

=====================================================================
"""

import functools
from datetime import datetime


# =====================================================================
# 1. FORMATTING DECORATORS
# Each decorator wraps a function that returns text and changes
# how that text looks, WITHOUT changing the function's own code.
# =====================================================================

def uppercase(func):
    """Decorator: converts the wrapped function's returned text to UPPERCASE."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs).upper()

    return wrapper


def bold(func):
    """Decorator: wraps returned text with markdown-style bold markers."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        return f"**{func(*args, **kwargs)}**"

    return wrapper


def add_border(char="-", length=50):
    """Decorator FACTORY: adds a top/bottom border made of `char`.
    Written as factory so the user can dynamically choose border style."""

    def decorator(func):

        @functools.wraps(func)
        def wrapper(*args, **kwargs):

            content = func(*args, **kwargs)

            border = char * length

            return f"{border}\n{content}\n{border}"

        return wrapper

    return decorator


def log_call(func):
    """Decorator: logs when a report-generating method starts/ends
    (useful for tracing report generation during a demo/viva)."""

    @functools.wraps(func)
    def wrapper(*args, **kwargs):

        print(f"[LOG] -> {func.__name__}() started")

        result = func(*args, **kwargs)

        print(f"[LOG] <- {func.__name__}() finished")

        return result

    return wrapper
# =====================================================================
# 2. REPORT SECTION (a simple helper class)
# =====================================================================

class ReportSection:
    """One section/heading of a report, e.g. 'Introduction', 'Results'."""

    def __init__(self, title, content):
        self.title = title
        self.content = content

    def __str__(self):          # MAGIC METHOD - readable form
        return f"{self.title}\n{self.content}"

    def __repr__(self):         # MAGIC METHOD - debug form
        return f"ReportSection(title={self.title!r})"

    def __eq__(self, other):    # MAGIC METHOD - equality
        return (
            isinstance(other, ReportSection)
            and self.title == other.title
            and self.content == other.content
        )


# =====================================================================
# 3. REPORT (the core dynamic report generator class)
# =====================================================================

class Report:
    """Dynamic, template-driven report generator."""

    # class-level registry shared by every Report -> supports classmethods
    _templates = {}

    def __init__(self, title, author="Unknown"):
        self.title = title
        self.author = author
        self.sections = []
        self.created_on = datetime.now()

    # -----------------------------------------------------------------
    # CLASS METHODS -> alternate constructors / template management
    # -----------------------------------------------------------------

    @classmethod
    def register_template(cls, name, section_titles):
        """Register a reusable report template (list of section titles)."""

        cls._templates[name] = section_titles

        print(f"[TEMPLATE] '{name}' registered with sections: {section_titles}")

    @classmethod
    def from_template(cls, name, title, author="Unknown"):
        """Alternate constructor: build a Report directly from a
        registered template name."""

        if name not in cls._templates:
            raise ValueError(f"Template '{name}' is not registered")

        report = cls(title, author)

        for sec_title in cls._templates[name]:
            report.add_section(sec_title, "<content pending>")

        return report

    @classmethod
    def available_templates(cls):
        return list(cls._templates.keys())

    # -----------------------------------------------------------------
    # INSTANCE METHODS
    # -----------------------------------------------------------------

    def add_section(self, title, content):

        self.sections.append(ReportSection(title, content))

        return self          # enables method chaining

    def set_content(self, title, content):
        """Fill in content for an existing (template-generated) section."""

        for sec in self.sections:

            if sec.title == title:

                sec.content = content

                return True

        return False

    @log_call
    @add_border("=", 50)
    def summary(self):
        """A short, decorator-formatted summary of the report."""

        return (
            f"Report: {self.title}\n"
            f"Author: {self.author}\n"
            f"Sections: {len(self.sections)}\n"
            f"Generated: {self.created_on:%Y-%m-%d %H:%M}"
        )

    @bold
    def title_line(self):
        return self.title
    @uppercase
    def author_line(self):
        return f"Author: {self.author}"

    # -----------------------------------------------------------------
    # MAGIC (DUNDER) METHODS
    # -----------------------------------------------------------------

    def __str__(self):
        """Human-readable report."""

        output = []
        output.append(self.title)
        output.append("=" * len(self.title))
        output.append(f"Author: {self.author}")
        output.append(f"Created: {self.created_on:%Y-%m-%d %H:%M}")
        output.append("")

        for section in self.sections:
            output.append(str(section))
            output.append("")

        return "\n".join(output)

    def __repr__(self):
        return (
            f"Report(title={self.title!r}, "
            f"author={self.author!r}, "
            f"sections={len(self.sections)})"
        )

    def __len__(self):
        """Number of sections."""
        return len(self.sections)

    def __getitem__(self, index):
        """Allow indexing."""
        return self.sections[index]

    def __iter__(self):
        """Allow iteration."""
        return iter(self.sections)

    def __contains__(self, title):
        """Check whether a section title exists."""
        return any(section.title == title for section in self.sections)

    def __add__(self, other):
        """Combine two reports."""

        if not isinstance(other, Report):
            return NotImplemented

        merged = Report(
            f"{self.title} + {other.title}",
            self.author
        )

        for section in self.sections:
            merged.add_section(section.title, section.content)

        for section in other.sections:
            merged.add_section(section.title, section.content)

        return merged

    def __eq__(self, other):
        """Compare reports."""

        return (
            isinstance(other, Report)
            and self.title == other.title
            and self.author == other.author
            and self.sections == other.sections
        )

    def __call__(self):
        """Calling the object prints the report."""

        print(self)
# =====================================================================
# 4. DEMO / DRIVER CODE
# =====================================================================

if __name__ == "__main__":

    # ---- Step A: register templates dynamically (classmethod) --------

    Report.register_template(
        "project_report",
        ["Introduction", "Methodology", "Results", "Conclusion"]
    )

    Report.register_template(
        "attendance_report",
        ["Summary", "Defaulter List"]
    )

    print("\nAvailable templates:", Report.available_templates())

    # ---- Step B: build a report FROM a template (classmethod ctor) ---

    r1 = Report.from_template(
        "project_report",
        "AI Lab Mini Project",
        author="Rahul"
    )

    r1.set_content(
        "Introduction",
        "This project explores dynamic report generation."
    )

    r1.set_content(
        "Methodology",
        "Used decorators, classmethods and magic methods."
    )

    r1.set_content(
        "Results",
        "Report generated and formatted successfully."
    )

    r1.set_content(
        "Conclusion",
        "OOP features simplify dynamic formatting."
    )

    # ---- Step C: build a second, manually-created report -------------

    r2 = Report(
        "Attendance Snapshot",
        author="Rahul"
    )

    r2.add_section(
        "Summary",
        "92% average attendance this month."
    )

    # ---- Step D: use magic methods ------------------------------------

    print("\n--- len(r1) ---")
    print(len(r1))          # __len__

    print("\n--- r1[0] ---")
    print(r1[0])            # __getitem__

    print("\n--- iterate over r1 ---")

    for section in r1:      # __iter__
        print(" •", section.title)

    print("\n--- 'Results' in r1 ---")
    print("Results" in r1)  # __contains__

    print("\n--- combine r1 + r2 ---")

    combined = r1 + r2      # __add__

    print(combined)         # __str__

    # ---- Step E: apply formatting decorators dynamically -------------

    print("\n--- decorated summary() [bordered + logged] ---")
    print(r1.summary())

    print("\n--- title_line() [bold] ---")
    print(r1.title_line())

    print("\n--- report as callable, formatted UPPERCASE on the fly ---")
    print(r1(formatter=str.upper))      # __call__ + dynamic formatter

    print("\n--- report as callable, default (no formatter) ---")
    print(r2())