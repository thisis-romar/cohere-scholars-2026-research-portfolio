# Data Analyst Upskilling Roadmap

This starter repository reframes the learning path for aspiring data analysts into four progressive pillars—Tableau, SQL, Python, and Excel—mirroring the layered curriculum highlighted in the reference graphic. Each pillar includes lesson goals, suggested hands-on tasks, and links to trusted documentation so the roadmap doubles as a living knowledge base.

## Overview of the Curriculum

| Pillar   | Lessons | Suggested Tasks | Focus |
|----------|---------|-----------------|-------|
| Tableau  | 19      | 32              | Visual analytics, dashboards, storytelling |
| SQL      | 14      | 33              | Relational querying, schema design, data governance |
| Python   | 35      | 141             | Data wrangling, analytics automation, reproducible workflows |
| Excel    | 12      | 48              | Spreadsheet modeling, data cleaning, executive reporting |

> **Tip:** Use the lesson counts as checkpoints. After completing each lesson series, document key takeaways and reusable assets (e.g., dashboards, query snippets, notebooks, templates) directly in this repository for future reference.

## Tableau Foundation (Start Here)

1. **Environment Setup** – Install Tableau Desktop or leverage Tableau Public.
2. **Connect to Data** – Practice pulling from flat files and relational sources.
3. **Visual Grammar** – Build charts (bar, line, scatter) and experiment with calculated fields.
4. **Dashboards & Stories** – Assemble interactive dashboards and storyboard narratives for stakeholders.
5. **Governance** – Publish to Tableau Server/Public and manage permissions.

**Documentation & References**
- [Tableau Help Portal](https://help.tableau.com/current/guides/everybody-install/en-us/everybody_install_installation.htm) – installation, data connections, and calculations.
- [Tableau Blueprint](https://www.tableau.com/learn/blueprint) – analytics workflows and adoption best practices.

## SQL Mastery (Second Pillar)

1. **Core Syntax** – SELECT, INSERT, UPDATE, DELETE, and filtering.
2. **Joins & Aggregations** – INNER/OUTER joins, GROUP BY, HAVING, window functions.
3. **Schema Design** – Normalize tables, define primary/foreign keys, and enforce constraints.
4. **Optimization** – Create indexes, analyze execution plans, and refactor queries for performance.
5. **Security & Governance** – Manage roles, apply row-level security, and audit access.

**Documentation & References**
- [PostgreSQL Documentation](https://www.postgresql.org/docs/current/sql.html) – SQL command reference and best practices.
- [SQL Server Learn](https://learn.microsoft.com/sql/?view=sql-server-ver16) – tutorials on T-SQL and database design fundamentals.

## Python for Analytics (Third Pillar)

1. **Project Scaffolding** – Set up virtual environments and package dependencies.
2. **Data Manipulation** – Use pandas for dataframes, cleaning, reshaping, and feature engineering.
3. **Visualization** – Create exploratory charts with Matplotlib and Seaborn.
4. **Automation** – Schedule ETL scripts, build reusable functions, and integrate APIs.
5. **Testing & Documentation** – Write unit tests (pytest) and document notebooks/reports.

**Documentation & References**
- [Python Documentation](https://docs.python.org/3/) – language reference, tutorials, and library index.
- [pandas User Guide](https://pandas.pydata.org/docs/user_guide/index.html) – data manipulation patterns and cookbook examples.
- [Matplotlib Tutorials](https://matplotlib.org/stable/tutorials/index.html) – plotting APIs and customization techniques.

## Excel for Operational Insight (Fourth Pillar)

1. **Model Building** – Construct reusable spreadsheet models with named ranges and structured references.
2. **Power Query & Power Pivot** – Automate data refreshes and build tabular models.
3. **Advanced Functions** – Master XLOOKUP, dynamic arrays, LET, and lambda functions.
4. **Visualization** – Build executive dashboards with pivot charts and conditional formatting.
5. **Collaboration** – Use shared workbooks, version history, and comments for stakeholder reviews.

**Documentation & References**
- [Microsoft Excel Training](https://support.microsoft.com/training/excel) – interactive learning paths and feature deep dives.
- [Microsoft Learn: Power Query](https://learn.microsoft.com/power-query/) – end-to-end data preparation guidance.

## Repository Usage Guidelines

- Create subdirectories for each pillar (`tableau/`, `sql/`, `python/`, `excel/`) to store artifacts, queries, notebooks, and templates.
- Track progress in a markdown journal (`progress-log.md`) noting completed lessons, blockers, and reflections.
- Capture findings from real datasets in case studies and link them in the `README` for quick navigation.
- When new tools enter your stack, append sections that mirror this structure and cite authoritative documentation.

## How to Contribute

1. Fork or clone this repository to your local machine.
2. Create feature branches for new artifacts or curriculum updates.
3. Commit changes with descriptive messages and open pull requests summarizing learning outcomes.
4. Review contributions for accuracy, reproducibility, and source citations before merging.

By grounding each learning pillar in primary documentation and actionable tasks, this repository evolves into comprehensive, vendor-agnostic documentation for your analytics journey.
