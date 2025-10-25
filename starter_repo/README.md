# Comprehensive Data Analytics Upskilling Blueprint

This repository curates a vendor-agnostic, citation-friendly roadmap for developing professional analytics skills across **Tableau**, **SQL**, **Python**, and **Excel**. It is structured so every milestone captures:

* learning outcomes linked to authoritative documentation;
* hands-on assets to archive in this repository (dashboards, queries, notebooks, spreadsheets);
* reflection prompts that translate individual lessons into reusable playbooks.

Use this blueprint to guide study plans, track deliverables, and build a demonstrable portfolio for analytics roles.

---

## 1. Curriculum Architecture

| Pillar  | Core Modules | Estimated Duration* | Portfolio Deliverables | Primary References |
|---------|--------------|---------------------|------------------------|--------------------|
| Tableau | 6 modules / 24 lessons | 4–5 weeks | Interactive dashboards, story workbooks, style guide | [Tableau Help](https://help.tableau.com/current/pro/desktop/en-us/pro_overview_desktop.htm), [Tableau Blueprint](https://www.tableau.com/learn/blueprint) |
| SQL     | 6 modules / 20 lessons | 4–6 weeks | Query library, ER diagrams, governance checklist | [PostgreSQL Docs](https://www.postgresql.org/docs/current/sql.html), [SQL Server Learn](https://learn.microsoft.com/sql/?view=sql-server-ver16) |
| Python  | 8 modules / 40 lessons | 6–8 weeks | Reproducible notebooks, automation scripts, test suites | [Python Docs](https://docs.python.org/3/), [pandas Guide](https://pandas.pydata.org/docs/user_guide/index.html), [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/index.html) |
| Excel   | 5 modules / 18 lessons | 3–4 weeks | Dynamic models, Power Query flows, executive dashboards | [Microsoft Excel Training](https://support.microsoft.com/training/excel), [Power Query Docs](https://learn.microsoft.com/power-query/) |

> \*Durations assume part-time study (~8–10 hours per week). Adjust pacing to suit prior experience.

---

## 2. Getting Started

1. **Set up the workspace**
   - Install Tableau Desktop (trial), Tableau Public, PostgreSQL, Python 3.11+, and Microsoft 365 or Excel standalone.
   - Configure a Python virtual environment (`python -m venv .venv`) and install baseline analytics packages (`pandas`, `numpy`, `matplotlib`, `seaborn`, `sqlalchemy`, `jupyter`).
   - Create the directory scaffold:
     ```
     starter_repo/
       tableau/
       sql/
       python/
       excel/
       projects/
       docs/
     ```

2. **Prepare sample datasets**
   - Download open datasets (e.g., [NOAA climate data](https://www.ncei.noaa.gov/), [IMF economic indicators](https://www.imf.org/en/Data), [UCI Machine Learning Repository](https://archive.ics.uci.edu/ml/index.php)).
   - Store raw data in `docs/data_sources.md` with source citations and refresh cadence.

3. **Adopt documentation standards**
   - Maintain a `progress-log.md` with lesson summaries, blockers, and next actions.
   - Capture experiment metadata (dataset, objective, metric) in README tables or dedicated markdown files.

---

## 3. Pillar Playbooks

Each playbook lists progressive modules. Use the **Suggested Assets** column to decide what to commit after finishing a lesson set. When possible, link source files and cite official documentation or public knowledge base articles consulted.

### 3.1 Tableau Analytics

| Module | Focus | Key Lessons | Suggested Assets | Additional References |
|--------|-------|-------------|-------------------|-----------------------|
| Foundation | Licensing, interface tour, data connections | Install Tableau, explore Show Me, connect CSV/Excel/SQL sources | `tableau/setup-notes.md`, connection cheatsheet | [Tableau Desktop Start](https://help.tableau.com/current/pro/desktop/en-us/gettingstarted_overview.htm) |
| Data Modeling | Relationships vs. joins, data interpreter, unions | Build logical/physical layer, manage extracts | Sample `.tds` and `.tdsx` files, data model diagrams | [Data Modeling in Tableau](https://help.tableau.com/current/pro/desktop/en-us/datasource_datamodel.htm) |
| Calculations | Calculated fields, table calcs, LOD expressions | Window calculations, parameter controls | Calculations catalog, parameterized dashboards | [Tableau Calculations](https://help.tableau.com/current/pro/desktop/en-us/calculations_calculatedfields_create.htm) |
| Visual Analytics | Chart selection, design best practices | Create bar, line, scatter, highlight tables, maps | Dashboard style guide (`docs/tableau-style.md`) | [Visual Best Practices](https://help.tableau.com/current/pro/desktop/en-us/best_practices_visual_design.htm) |
| Dashboards & Stories | Layout containers, actions, storytelling | Interactive dashboards, story points, device designer | Publish-ready dashboards in `tableau/dashboards/` | [Dashboard Actions](https://help.tableau.com/current/pro/desktop/en-us/actions.htm) |
| Governance & Sharing | Permissions, data server, Tableau Public | Set up projects, certify data, document refresh | Deployment checklist, governance charter | [Tableau Server Admin](https://help.tableau.com/current/server/en-us/get_started_server.htm) |

**Milestone Project:** Create a multi-page dashboard analyzing economic indicators across regions, include calculated KPIs, parameters, and story narration.

### 3.2 SQL Engineering

| Module | Focus | Key Lessons | Suggested Assets | Additional References |
|--------|-------|-------------|-------------------|-----------------------|
| Query Fundamentals | SELECT, WHERE, ORDER BY, LIMIT | Filter, sort, alias columns | `sql/00-select-basics.sql` with annotated queries | [PostgreSQL Tutorial](https://www.postgresql.org/docs/current/tutorial-select.html) |
| Joins & Aggregations | INNER/OUTER joins, GROUP BY, HAVING | Combine tables, aggregate metrics | Join patterns notebook, ER diagram (`docs/sql-schema.drawio`) | [Joins Tutorial](https://learn.microsoft.com/sql/t-sql/queries/from-using-join-transact-sql?view=sql-server-ver16) |
| Subqueries & CTEs | Derived tables, recursive queries | Window functions, ranking, partitions | `sql/02-advanced-queries.sql`, query performance notes | [PostgreSQL CTE](https://www.postgresql.org/docs/current/queries-with.html) |
| Data Modeling | Normal forms, constraints, indexing | Design star schema, enforce integrity | Schema migration scripts, metadata dictionary | [Database Design Basics](https://learn.microsoft.com/sql/relational-databases/database-design?view=sql-server-ver16) |
| Performance Tuning | EXPLAIN plans, indexing strategies | Identify bottlenecks, refactor queries | Performance logbook (`docs/sql-performance.md`) | [PostgreSQL Performance Tips](https://www.postgresql.org/docs/current/performance-tips.html) |
| Security & Governance | Roles, privileges, data masking | Auditing, compliance, backup strategy | Access control matrix, backup scripts | [SQL Security Best Practices](https://learn.microsoft.com/sql/relational-databases/security/securing-sql-server?view=sql-server-ver16) |

**Milestone Project:** Build a normalized warehouse for the chosen dataset, populate it with ETL scripts, and expose analytical views for Tableau and Excel consumers.

### 3.3 Python for Data Analytics

| Module | Focus | Key Lessons | Suggested Assets | Additional References |
|--------|-------|-------------|-------------------|-----------------------|
| Environment & Tooling | Virtualenv, dependency management, packaging | Poetry/pip-tools, linting (flake8), formatting (black) | `python/requirements.txt`, `pyproject.toml`, setup notes | [Python Packaging User Guide](https://packaging.python.org/en/latest/tutorials/installing-packages/) |
| Data Acquisition | File I/O, APIs, web scraping | Requests, authentication, pagination | Data ingestion scripts, credential handling checklist | [Requests Quickstart](https://requests.readthedocs.io/en/latest/user/quickstart/) |
| Data Wrangling | pandas indexing, reshaping, missing data | `groupby`, merging, feature engineering | Notebook library (`python/notebooks/`) with markdown commentary | [pandas Cookbooks](https://pandas.pydata.org/docs/user_guide/cookbook.html) |
| Exploratory Analysis | Descriptive stats, visualization, profiling | seaborn pairplots, pandas profiling reports | EDA templates, profiling exports (`docs/eda/`) | [Seaborn Tutorials](https://seaborn.pydata.org/tutorial.html) |
| Automation & Pipelines | Scheduling, modular functions, CLI | Build ETL pipeline with logging and config files | CLI script (`python/pipelines/`), Airflow or Prefect notes | [Airflow Concepts](https://airflow.apache.org/docs/apache-airflow/stable/concepts/index.html) |
| Testing & Quality | pytest, fixtures, data validation | Great Expectations or pandera checks | `tests/` folder with unit and data quality tests | [pytest Documentation](https://docs.pytest.org/en/stable/) |
| Reporting & Delivery | Notebook-to-report conversion, storytelling | nbconvert, papermill, parameterized notebooks | Automated report script, narrative template | [Jupyter nbconvert](https://nbconvert.readthedocs.io/en/latest/) |
| Deployment | Packaging, CI/CD, containerization | GitHub Actions, Docker basics | CI workflow file, Dockerfile for analytics app | [GitHub Actions Docs](https://docs.github.com/actions) |

**Milestone Project:** Deliver an automated analytics pipeline: ingest raw data, clean and validate it, generate dashboards or reports, and publish outputs to Tableau or Excel.

### 3.4 Excel for Decision Support

| Module | Focus | Key Lessons | Suggested Assets | Additional References |
|--------|-------|-------------|-------------------|-----------------------|
| Foundations & Interface | Named ranges, tables, keyboard efficiency | Workbook organization, data validation | Template workbook with documentation tab | [Excel Basic Tasks](https://support.microsoft.com/office/excel-video-training-9bc05390-e94c-46af-a5b3-d7c22f6990bb) |
| Data Cleaning & Shaping | Power Query transformations, text functions | Automate refresh, combine files, conditional logic | Power Query `.pq` files, cleaning checklist | [Power Query Overview](https://learn.microsoft.com/power-query/power-query-what-is-power-query) |
| Analysis Functions | Lookup functions, dynamic arrays, statistical tools | XLOOKUP, FILTER, LET, LAMBDA, Analysis ToolPak | Function reference sheets, scenario planner workbook | [Dynamic Arrays Guide](https://support.microsoft.com/office/dynamic-array-formulas-and-spilled-array-behavior-4dbe79d3-8c79-4903-9b4e-c3b72aa023bd) |
| Visualization & Dashboards | PivotTables, charts, slicers, KPIs | Conditional formatting, sparklines, themes | Executive dashboard template, color palette guide | [Create a PivotTable](https://support.microsoft.com/office/create-a-pivottable-to-analyze-worksheet-data-a9a84538-bfe9-40a9-a8e9-f99134456576) |
| Collaboration & Governance | Shared workbooks, OneDrive, version history | Data protection, sensitivity labels, macros policies | Collaboration SOP, macro review checklist | [Protect an Excel File](https://support.microsoft.com/office/password-protect-documents-workbooks-and-presentations-ef163677-319a-44fb-bd9e-677d1e9aa448) |

**Milestone Project:** Construct a scenario modeling workbook linked to Power Query sources, with documentation for assumptions, refresh cadence, and stakeholder presentation notes.

---

## 4. Cross-Pillar Integration Projects

1. **Data Quality Audit:** Ingest raw data with Python, validate with SQL constraints, visualize issues in Tableau, and summarize remediation steps in Excel.
2. **Executive KPI Suite:** Design a star schema in SQL, build automated Python ETL jobs, surface dashboards in Tableau, and craft printable Excel scorecards.
3. **Self-Service Analytics Kit:** Package parameterized Python notebooks, publish Tableau dashboards, distribute Excel templates, and document usage in `docs/user-guide.md`.

Capture each project in the `projects/` directory with:

- `README.md` summarizing objectives, architecture diagram, and outcome metrics.
- Links to datasets, scripts, dashboards, and stakeholder-ready assets.
- Retrospective notes outlining lessons learned and next steps.

---

## 5. Documentation & Citation Standards

* **Source Attribution:** For every external article or tutorial consulted, add a bullet with the URL and access date in the relevant README or notebook.
* **Versioning:** Note software versions (e.g., Tableau 2023.3, Python 3.11.6) at the top of lesson notes to maintain reproducibility.
* **Change Logs:** Use `docs/changelog.md` to summarize weekly updates and tie commits to learning outcomes.
* **Templates:**
  - `docs/templates/progress-log-template.md`
  - `docs/templates/project-retro-template.md`
  - `docs/templates/dashboard-documentation.md`

Populate templates as you progress to keep the repository audit-ready.

---

## 6. Contribution Workflow

1. **Branching:** Create feature branches per pillar or project (e.g., `feature/tableau-dashboards`).
2. **Commits:** Write descriptive messages capturing the learning artifact and referenced documentation.
3. **Pull Requests:** Summarize goals, attach screenshots of dashboards or Excel models, and list data sources with citations.
4. **Reviews:** Validate reproducibility (scripts run, dashboards refresh), verify documentation completeness, and ensure all external references are cited.
5. **Automation:** Configure CI checks (linting, tests, workbook validation) as the repository matures to maintain quality.

---

## 7. Progress Tracking Checklist

- [ ] Set up local environment and repository scaffold.
- [ ] Catalog datasets with sources and refresh cadence.
- [ ] Complete Tableau foundation modules and publish first dashboard.
- [ ] Build SQL schema, ingest sample data, and document governance.
- [ ] Deliver Python EDA notebook with automated report.
- [ ] Produce Excel executive dashboard with refresh instructions.
- [ ] Execute at least one cross-pillar integration project.
- [ ] Update changelog, templates, and reflections with citations.

By iteratively following these modules and documenting each artifact, you will assemble a comprehensive, well-cited analytics portfolio demonstrating fluency in visualization, data engineering, automation, and stakeholder reporting.
