#!/usr/bin/env python3
"""
Generate Black Wave Capability Statement PDF
"""

from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.lib.colors import HexColor
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, PageBreak, Image, Table, TableStyle, PageTemplate, BaseDocTemplate, Frame, NextPageTemplate
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas
from reportlab.lib.utils import ImageReader
import os

# Color scheme matching website
COLOR_BG = HexColor('#050505')
COLOR_TEXT = HexColor('#e6ddc7')
COLOR_ACCENT = HexColor('#c89a3c')
COLOR_MUTED = HexColor('#aca08a')

# Image paths
SHOWCASE_IMAGE = 'assets/img/BW_website-service_showcase_2.png'
HERO_IMAGE = 'assets/img/BW_website-hero.png'
LOGO_IMAGE = 'assets/img/Final_Logo.png'

def draw_cover_page(canvas_obj, doc):
    """Draw the showcase image as full-page background for page 1"""
    width, height = letter
    
    if os.path.exists(SHOWCASE_IMAGE):
        canvas_obj.saveState()
        # Draw image to fill entire page
        canvas_obj.drawImage(SHOWCASE_IMAGE, 0, 0, width=width, height=height, 
                           preserveAspectRatio=True, mask='auto')
        canvas_obj.restoreState()

def draw_content_page(canvas_obj, doc):
    """Draw hero background and logo for pages 2+"""
    width, height = letter
    
    canvas_obj.saveState()
    
    # Draw hero image as background with dark overlay
    if os.path.exists(HERO_IMAGE):
        canvas_obj.drawImage(HERO_IMAGE, 0, 0, width=width, height=height, 
                           preserveAspectRatio=True, mask='auto')
        # Add dark overlay to make text readable
        canvas_obj.setFillColor(HexColor('#000000'))
        canvas_obj.setFillAlpha(0.85)
        canvas_obj.rect(0, 0, width, height, fill=1, stroke=0)
    
    # Draw logo in top left corner
    if os.path.exists(LOGO_IMAGE):
        logo_size = 1.2 * inch
        logo_x = 0.5 * inch
        logo_y = height - 0.5 * inch - logo_size
        canvas_obj.drawImage(LOGO_IMAGE, logo_x, logo_y, width=logo_size, height=logo_size, 
                           preserveAspectRatio=True, mask='auto')
    
    canvas_obj.restoreState()

def create_capability_statement():
    """Generate the Black Wave Capability Statement PDF"""
    
    # Create PDF document with custom page templates
    pdf_path = 'capability_statement.pdf'
    
    # Create frames for content (will be set after doc creation)
    left_margin = 0.75*inch
    right_margin = 0.75*inch
    top_margin = 0.75*inch
    bottom_margin = 0.75*inch
    width, height = letter
    
    frame = Frame(
        left_margin,
        bottom_margin,
        width - left_margin - right_margin,
        height - top_margin - bottom_margin,
        leftPadding=0,
        bottomPadding=0,
        rightPadding=0,
        topPadding=0,
        id='normal'
    )
    
    # Create page templates
    cover_template = PageTemplate(id='cover', frames=[frame], onPage=draw_cover_page)
    content_template = PageTemplate(id='content', frames=[frame], onPage=draw_content_page)
    
    doc = BaseDocTemplate(
        pdf_path,
        pagesize=letter,
        rightMargin=right_margin,
        leftMargin=left_margin,
        topMargin=top_margin,
        bottomMargin=bottom_margin,
        pageTemplates=[cover_template, content_template]
    )
    
    # Container for the 'Flowable' objects
    story = []
    
    # Define styles
    styles = getSampleStyleSheet()
    
    # Custom styles with better contrast for overlay backgrounds
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Heading1'],
        fontSize=28,
        textColor=COLOR_ACCENT,
        spaceAfter=30,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold',
        backColor=HexColor('#000000'),
        borderPadding=10
    )
    
    heading_style = ParagraphStyle(
        'CustomHeading',
        parent=styles['Heading2'],
        fontSize=20,
        textColor=COLOR_ACCENT,
        spaceAfter=12,
        spaceBefore=20,
        fontName='Helvetica-Bold',
        backColor=HexColor('#000000'),
        borderPadding=8
    )
    
    subheading_style = ParagraphStyle(
        'CustomSubheading',
        parent=styles['Heading3'],
        fontSize=14,
        textColor=COLOR_ACCENT,
        spaceAfter=8,
        spaceBefore=12,
        fontName='Helvetica-Bold',
        backColor=HexColor('#000000'),
        borderPadding=6
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=11,
        textColor=COLOR_TEXT,
        spaceAfter=12,
        alignment=TA_JUSTIFY,
        leading=14,
        backColor=HexColor('#000000'),
        borderPadding=8
    )
    
    bullet_style = ParagraphStyle(
        'CustomBullet',
        parent=styles['Normal'],
        fontSize=10,
        textColor=COLOR_TEXT,
        spaceAfter=8,
        leftIndent=20,
        bulletIndent=10,
        leading=13,
        backColor=HexColor('#000000'),
        borderPadding=6
    )
    
    # ============ PAGE 1: Cover with Showcase Image ============
    # Use cover template (showcase image background)
    story.append(Spacer(1, 2*inch))
    
    # Add text overlay on showcase image with semi-transparent background
    story.append(Paragraph(
        "Black Wave",
        ParagraphStyle(
            'CoverTitle',
            parent=styles['Heading1'],
            fontSize=36,
            textColor=COLOR_ACCENT,
            alignment=TA_CENTER,
            spaceAfter=20,
            fontName='Helvetica-Bold',
            backColor=HexColor('#000000'),
            borderPadding=15
        )
    ))
    
    story.append(Paragraph(
        "Construction & Decision Science",
        ParagraphStyle(
            'CoverSubtitle',
            parent=styles['Normal'],
            fontSize=18,
            textColor=COLOR_TEXT,
            alignment=TA_CENTER,
            spaceAfter=40,
            backColor=HexColor('#000000'),
            borderPadding=10
        )
    ))
    
    story.append(Paragraph(
        "Capability Statement",
        ParagraphStyle(
            'CapabilityTitle',
            parent=styles['Normal'],
            fontSize=24,
            textColor=COLOR_ACCENT,
            alignment=TA_CENTER,
            spaceAfter=50,
            fontName='Helvetica-Bold',
            backColor=HexColor('#000000'),
            borderPadding=12
        )
    ))
    
    # Switch to content template for remaining pages
    story.append(NextPageTemplate('content'))
    story.append(PageBreak())
    story.append(Spacer(1, 0.2*inch))
    
    # ============ PAGE 2: About Black Wave ============
    story.append(Paragraph("About Black Wave", heading_style))
    
    story.append(Paragraph(
        "Black Wave is a Service-Disabled Veteran-Owned small business that began as a "
        "boots-on-the-ground construction firm. We have delivered work in demanding environments "
        "where mission, safety, and reliability matter more than anything else.",
        body_style
    ))
    
    story.append(Paragraph(
        "Over time, we added deep decision science and GenAI capabilities to tackle persistent "
        "challenges in planning, logistics, and communication. Today, we bring both disciplines "
        "to every engagement—so owners never have to choose between practical execution and "
        "advanced analytics.",
        body_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("What Sets Us Apart", subheading_style))
    
    story.append(Paragraph("• Service-Disabled Veteran-Owned Small Business (SDVOSB)", bullet_style))
    story.append(Paragraph("• Experience supporting federal, DoD, and research environments", bullet_style))
    story.append(Paragraph("• Hands-on construction background plus advanced analytics expertise", bullet_style))
    story.append(Paragraph("• 25+ years of mission-aligned delivery", bullet_style))
    
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph(
        "Black Wave's decision science and GenAI work comes directly from field pain points: "
        "schedule risk, logistics, RFIs, and complex stakeholder environments. We build tools "
        "that speak the language of projects, not just the language of data.",
        body_style
    ))
    
    story.append(PageBreak())
    
    # ============ PAGE 3: Construction Services ============
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Construction Services", heading_style))
    
    story.append(Paragraph(
        "General construction and renovations delivered by a SDVOSB with hands-on experience "
        "in demanding federal and commercial environments.",
        body_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Our Construction Capabilities", subheading_style))
    
    story.append(Paragraph("• Construction management services", bullet_style))
    story.append(Paragraph("• Site work and civil construction", bullet_style))
    story.append(Paragraph("• Infrastructure, utilities, and ISP/OSP", bullet_style))
    story.append(Paragraph("• Mission-critical and secure facilities", bullet_style))
    story.append(Paragraph("• General construction and renovations", bullet_style))
    story.append(Paragraph("• Tenant improvements and build-outs", bullet_style))
    
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Service Offerings", subheading_style))
    
    story.append(Paragraph(
        "<b>General Construction & Renovations</b><br/>"
        "Best for facility upgrades, tenant improvements, and infrastructure work in active environments.",
        body_style
    ))
    
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph(
        "<b>Mission-Critical & Secure Spaces</b><br/>"
        "Build-outs and improvements where uptime, security, and reliability are non-negotiable.",
        body_style
    ))
    
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph(
        "<b>Owner's Representative / Advisory</b><br/>"
        "Field-savvy representation that connects design intent, contracts, and on-site realities.",
        body_style
    ))
    
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Past Performance Highlights", subheading_style))
    
    story.append(Paragraph(
        "<b>Renovation of Mission Support Facility</b><br/>"
        "Federal Agency • Role: Prime Contractor<br/>"
        "Multi-phase renovation of an active mission support facility, including interior build-out "
        "and systems coordination. Maintained operations with minimal downtime and delivered on time "
        "despite constrained access windows.",
        body_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph(
        "<b>Secure Operations Center Build-Out</b><br/>"
        "DoD Installation • Role: Subcontractor<br/>"
        "Build-out of a secure operations space with specialized mechanical, electrical, and IT "
        "infrastructure requirements. Coordinated with multiple trades and security stakeholders, "
        "meeting strict commissioning and acceptance milestones.",
        body_style
    ))
    
    story.append(PageBreak())
    
    # ============ PAGE 4: Decision Science Services ============
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Decision Science Services", heading_style))
    
    story.append(Paragraph(
        "Designing advanced analytics and GenAI to improve planning, logistics, and project "
        "decision-making across your portfolio.",
        body_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Our Decision Science Capabilities", subheading_style))
    
    story.append(Paragraph("• Strategic resource allocation optimization", bullet_style))
    story.append(Paragraph("• Efficient operational & logistics planning", bullet_style))
    story.append(Paragraph("• Executive dashboards & scenario analysis", bullet_style))
    story.append(Paragraph("• Work packaging and phasing optimization", bullet_style))
    story.append(Paragraph("• AI-enabled planning for capital projects", bullet_style))
    story.append(Paragraph("• GenAI-supported workflows for project analysis", bullet_style))
    
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Service Offerings", subheading_style))
    
    story.append(Paragraph(
        "<b>Project Intelligence</b><br/>"
        "Dashboards and analytics that highlight risk, progress, and decision points for leadership "
        "and field teams.",
        body_style
    ))
    
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph(
        "<b>Workflow Design</b><br/>"
        "Standard operating procedures and playbooks with GenAI support for RFIs, submittals, "
        "and schedule planning.",
        body_style
    ))
    
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph(
        "<b>Strategic Support</b><br/>"
        "Mission engineering, scenario analysis, and portfolio-level insight for complex programs.",
        body_style
    ))
    
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("KELLI AI Platform", heading_style))
    
    story.append(Paragraph(
        "<b>Knowledge Executive with Large Language Insights</b>",
        subheading_style
    ))
    
    story.append(Paragraph(
        "Black Wave employs the KELLI AI platform as a core component of our decision science "
        "capabilities. KELLI AI serves as the agentic facilitator and orchestrator with "
        "comprehension of all organizational workflows. Rather than replacing workflows, KELLI AI "
        "maintains context, makes latent connections, facilitates hand-offs, and surfaces "
        "cross-workflow insights.",
        body_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Key Capabilities", subheading_style))
    
    story.append(Paragraph(
        "<b>Context Preservation</b><br/>"
        "Preserves rich context from one workflow as it feeds into another, ensuring continuity "
        "and preventing information loss. Enables seamless transitions between teams and processes.",
        body_style
    ))
    
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph(
        "<b>Cross-Workflow Insights</b><br/>"
        "Discovers patterns across multiple workflows, enabling analysis that spans organization "
        "sectors and revealing opportunities only visible at the orchestration level.",
        body_style
    ))
    
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph(
        "<b>Latent Connection Discovery</b><br/>"
        "Identifies relationships between disconnected efforts, connects strategic planning with "
        "operational needs, and links trends analysis with opportunity assessment.",
        body_style
    ))
    
    story.append(Spacer(1, 0.15*inch))
    
    story.append(Paragraph(
        "<b>Multi-Workflow Orchestration</b><br/>"
        "Facilitates coordination across environmental scanning, strategic planning, scenario "
        "development, trends analysis, and execution workflows, ensuring alignment and efficiency.",
        body_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph(
        "KELLI AI enables Black Wave to deliver intelligent decision support that understands "
        "the full context of your organization's operations, connecting strategic objectives "
        "with tactical execution for superior project outcomes.",
        body_style
    ))
    
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Past Performance Highlights", subheading_style))
    
    story.append(Paragraph(
        "<b>AI-Enabled Planning for Capital Projects</b><br/>"
        "Federal Program Office • Role: Decision Science Advisor<br/>"
        "Developed GenAI-supported workflows for analyzing project options, schedule risk, and "
        "resource trade-offs. Reduced planning cycle time by approximately 40% and created reusable "
        "decision frameworks for future projects.",
        body_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph(
        "<b>Logistics & Work Packaging Optimization</b><br/>"
        "DoD Facilities Portfolio • Role: Analytics Lead<br/>"
        "Applied analytics and GenAI tooling to evaluate work packaging, staging, and material "
        "flows across multiple sites. Improved material utilization and reduced idle time, enabling "
        "clearer communication to field teams and leadership.",
        body_style
    ))
    
    story.append(PageBreak())
    
    # ============ PAGE 5: Why Both Together ============
    story.append(Spacer(1, 0.2*inch))
    story.append(Paragraph("Why Construction and GenAI Belong Together", heading_style))
    
    story.append(Paragraph(
        "Black Wave's unique combination of construction expertise and decision science capabilities "
        "creates a powerful synergy that delivers superior project outcomes.",
        body_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Field-Driven AI, Not Hype", subheading_style))
    
    story.append(Paragraph(
        "Our analytics and GenAI workflows are grounded in actual project constraints, phasing, "
        "and safety requirements—not abstract algorithms in isolation. Every tool we build addresses "
        "real challenges faced in the field.",
        body_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph("Smarter Projects, Not Just Smarter Slides", subheading_style))
    
    story.append(Paragraph(
        "Insights feed back into real jobs: better planning, clearer communication, and fewer "
        "surprises for owners and field teams. Our decision science work directly improves project "
        "execution and outcomes.",
        body_style
    ))
    
    story.append(Spacer(1, 0.3*inch))
    
    story.append(Paragraph("Our Core Principles", subheading_style))
    
    story.append(Paragraph("• Safety & quality first", bullet_style))
    story.append(Paragraph("• Evidence-based use of AI", bullet_style))
    story.append(Paragraph("• Mission-aligned, responsible tech", bullet_style))
    story.append(Paragraph("• Practical execution meets advanced analytics", bullet_style))
    
    story.append(Spacer(1, 0.4*inch))
    
    # Contact information
    story.append(Paragraph("Contact Information", subheading_style))
    
    story.append(Paragraph(
        "For more information about Black Wave's capabilities or to discuss your project needs, "
        "please visit our website or contact us directly.",
        body_style
    ))
    
    story.append(Spacer(1, 0.2*inch))
    
    story.append(Paragraph(
        "<b>Service-Disabled Veteran-Owned Small Business (SDVOSB)</b>",
        ParagraphStyle(
            'Contact',
            parent=styles['Normal'],
            fontSize=11,
            textColor=COLOR_ACCENT,
            alignment=TA_CENTER,
            spaceAfter=20,
            backColor=HexColor('#000000'),
            borderPadding=8
        )
    ))
    
    # Build PDF
    doc.build(story)
    print(f"Capability statement PDF generated: {pdf_path}")
    return pdf_path

if __name__ == '__main__':
    create_capability_statement()
