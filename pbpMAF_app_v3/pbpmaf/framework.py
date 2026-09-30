"""Population Based Planning Maturity Assessment Framework (pbpMAF) content.

Themes, subthemes and characteristics of high maturity, the Steps to Maturity
scale and the reference lists used by the app. Edit the wording here; the app
and the notebook both read from this module.
"""

STEPS = [
    "Not at all",
    "To a Small Extent",
    "Moderately",
    "To a Large Extent",
    "Full",
]

# Steps treated as lower maturity and flagged for regional discussion.
LOWER_MATURITY_STEPS = ["Not at all", "To a Small Extent"]

HEALTH_REGIONS = [
    "HSE Dublin and North East",
    "HSE Dublin and Midlands",
    "HSE Dublin and South East",
    "HSE South West",
    "HSE Mid West",
    "HSE West and North West",
]

ASSESSMENT_LEVELS = [
    "CHA",
    "care group",
    "network of care",
    "PBP steering group",
]

CROSS_CUTTING_CONCEPTS = [
    "Equity",
    "Capacity building",
    "Continuous improvement",
    "Organisational culture",
    "Transparency and accountability",
]

THEMES = [
    {
        "theme": "Leadership and Governance",
        "subthemes": [
            {
                "subtheme": "Establishment and mandate",
                "characteristics": [
                    "Formally established leadership and governance structures. There is shared ownership which is supported by clearly defined roles and responsibilities",
                    "Leadership has a mandate to implement the programme",
                ],
            },
            {
                "subtheme": "Leadership support and commitment",
                "characteristics": [
                    "Cohesive and visible leadership support and commitment",
                    "Leaders actively champion programme implementation",
                ],
            },
            {
                "subtheme": "Vision and culture",
                "characteristics": [
                    "Leadership creates a culture that supports change, continuous improvement and innovation",
                    "Effective communication of the shared vision across the organisation",
                ],
            },
            {
                "subtheme": "Accountability, equity and transparency",
                "characteristics": [
                    "Management strategy and processes are in place to manage conflicts of interest, competing priorities and handling trade-offs",
                    "Transparent and ethical decision-making processes are in place. Equity is prioritised, attention is given to areas of greatest need, value and impact.",
                    "Risks of programme implementation have been identified and proportionally mitigated",
                    "Leadership provides oversight without creating unnecessary delay",
                ],
            },
        ],
    },
    {
        "theme": "Integration and Delivery",
        "subthemes": [
            {
                "subtheme": "Strategy and processes",
                "characteristics": [
                    "Programme implementation strategy is developed and is aligned with the programme objectives",
                    "The strategy can be translated into targeted and specific action items",
                    "Standardised and coordinated processes are in place and are reviewed and updated regularly",
                ],
            },
            {
                "subtheme": "Integration",
                "characteristics": [
                    "The programme is integrated across the organisation and is seen as one of the organisation's core components",
                    "The programme's objectives are considered in organisation-wide decision making at all levels and is integrated into routine activities, systems and processes",
                ],
            },
            {
                "subtheme": "Evidence-informed decision making",
                "characteristics": [
                    "Decision-making and recommendations are informed by the full range of available evidence, including qualitative data, quantitative data, lived experience, monitoring and evaluation evidence, and best practice.",
                    "An equity lens is applied to decision making processes",
                ],
            },
            {
                "subtheme": "Translating into action",
                "characteristics": [
                    "Recommendations and decisions are consistently actioned and result in change.",
                    "High rates of project completion and sustained momentum for change",
                ],
            },
        ],
    },
    {
        "theme": "Resources and Funding",
        "subthemes": [
            {
                "subtheme": "Planning and capacity building",
                "characteristics": [
                    "Current and future resource requirements are sufficiently planned for",
                    "Future planning incorporates capacity building",
                    "Resource planning is informed by a clear understanding of the strengths, weaknesses and gaps in the resources and infrastructure.",
                    "Funding and capabilities are already in place",
                ],
            },
            {
                "subtheme": "Sustainable allocation of funding and resources",
                "characteristics": [
                    "Commitment of sufficient funding which includes funding for initial upfront investment through to long-term sustainability and capacity building",
                    "Maintains service continuity during periods of increased demand",
                ],
            },
            {
                "subtheme": "Workforce capability and expertise",
                "characteristics": [
                    "Access to skilled and expert workforce and plans for continued investment in the workforce",
                    "Workforce capability and capacity is routinely monitored and developed to ensure ability to meet current and future demands",
                ],
            },
        ],
    },
    {
        "theme": "Workforce Support and Development",
        "subthemes": [
            {
                "subtheme": "Workforce training and professional development",
                "characteristics": [
                    "Organisation provides structured training and professional development opportunities",
                    "Systems and processes in place to support workforce professional development",
                ],
            },
            {
                "subtheme": "Culture of learning and continuous improvement",
                "characteristics": [
                    "Leaders and managers demonstrate coaching and supportive leadership style",
                    "Culture and systems in place to support ongoing learning and continuous improvement",
                ],
            },
        ],
    },
    {
        "theme": "Infrastructure and Information Systems",
        "subthemes": [
            {
                "subtheme": "Physical and technical infrastructure",
                "characteristics": [
                    "Physical and technical infrastructure is in place which enables effective programme and service integration and delivery",
                ],
            },
            {
                "subtheme": "Integrated and interoperable information systems",
                "characteristics": [
                    "Shared, integrated and interoperable regional and national information systems",
                    "Information governance and data sharing arrangements support secure and effective use of data",
                ],
            },
            {
                "subtheme": "Data availability and quality",
                "characteristics": [
                    "Access to regional, national and global databases, including access to raw data when required",
                    "Access to qualitative data and data on lived experience",
                    "Datasets are complete and accurate, providing a whole-system view",
                    "Relevant stakeholders routinely contribute to and use shared information systems",
                ],
            },
            {
                "subtheme": "Analytical Capability",
                "characteristics": [
                    "Access to skilled analytical expertise",
                    "Ability to analyse data to generate information required for programme planning, implementation, delivery, monitoring, and improvement",
                ],
            },
        ],
    },
    {
        "theme": "Stakeholder Engagement",
        "subthemes": [
            {
                "subtheme": "Formalised interagency partnerships",
                "characteristics": [
                    "Formalised partnerships with external stakeholders across organisational and agency boundaries",
                    "Work with stakeholders to develop sustainable business models",
                    "Visible stakeholder engagement",
                ],
            },
            {
                "subtheme": "Exchange of information and collaboration",
                "characteristics": [
                    'Leaders and managers undertake "go and see" visits to external bodies',
                    "Exchange of information and effective collaboration with stakeholders",
                ],
            },
            {
                "subtheme": "Support of politicians and policy makers",
                "characteristics": [
                    "Political support for the programme and engagement with policymakers",
                ],
            },
        ],
    },
    {
        "theme": "Monitoring and Improving",
        "subthemes": [
            {
                "subtheme": "Built-in evaluation frameworks",
                "characteristics": [
                    "Built-in processes and frameworks are in place to monitor programme outcomes and impact",
                    "A systematic approach is used to evaluate programme and service",
                ],
            },
            {
                "subtheme": "Defined measures of success",
                "characteristics": [
                    "Clear, consistent and predefined measures of success and timeframes against which programme outcomes and impact are assessed",
                ],
            },
            {
                "subtheme": "Audit and review",
                "characteristics": [
                    "Regular audits and reviews conducted to assess programme effectiveness and impact",
                    "Results of audit are available, transparent and effectively disseminated",
                ],
            },
            {
                "subtheme": "Continuous improvement cycle",
                "characteristics": [
                    "Processes in place to ensure results and recommendations of audits and reviews are acted on",
                    "Established cycle of continuous improvement",
                ],
            },
        ],
    },
    {
        "theme": "Citizen Engagement and Empowerment",
        "subthemes": [
            {
                "subtheme": "Collaboration between professionals, citizens, communities and service users",
                "characteristics": [
                    "Professionals, citizens and communities collaborate to co-design solutions and best models for change",
                    "Meaningful, inclusive and representative involvement of citizens and service users is embedded through-out decision-making processes and implementation",
                ],
            },
            {
                "subtheme": "Guided by lived experience",
                "characteristics": [
                    "Lived experience of staff and service users guide service modelling and decision-making process",
                ],
            },
            {
                "subtheme": "Public support",
                "characteristics": [
                    "There is public support for the programme",
                ],
            },
        ],
    },
]


def subtheme_key(theme_index: int, subtheme_index: int) -> str:
    """Stable identifier for a subtheme, e.g. 't1s2' (1-based)."""
    return f"t{theme_index + 1}s{subtheme_index + 1}"


def iter_subthemes():
    """Yield (key, theme_number, theme, subtheme_number, subtheme, characteristics)."""
    for ti, theme in enumerate(THEMES):
        for si, sub in enumerate(theme["subthemes"]):
            yield (
                subtheme_key(ti, si),
                ti + 1,
                theme["theme"],
                si + 1,
                sub["subtheme"],
                sub["characteristics"],
            )
