{
    'name': 'Enterprise Financial Automation & Controls',
    'version': '18.0.1.0.0',
    'category': 'Productivity/AI',
    'summary': 'AI-driven financial close automation, internal controls, and real-time audit trails.',
    'description': """
        Enterprise Financial Automation & Controls
        ============================================
        Transform your financial operations with AI-powered automation:

        - Automated period-end close with task orchestration
        - AI anomaly detection on journal entries and GL balances
        - Segregation of duties (SoD) enforcement and conflict alerts
        - Real-time internal controls testing and compliance scoring
        - Multi-entity consolidation with intercompany eliminations
        - Smart reconciliation engine with auto-matching
        - Audit trail with immutable transaction history
        - Executive financial dashboards with drill-down analytics
    """,
    'author': 'SoftaiDev',
    'website': 'https://softaidev.pages.dev',
    'license': 'LGPL-3',
    'price': 1299.99,
    'currency': 'USD',
    'depends': ['base', 'web', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'views/financial_close_views.xml',
        'views/internal_control_views.xml',
        'views/anomaly_detection_views.xml',
        'views/consolidation_views.xml',
        'views/reconciliation_views.xml',
        'views/menu.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
