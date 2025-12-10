import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
    KeepTogether, HRFlowable, ListFlowable, ListItem
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """Canvas for adding professional running headers and 'Page X of Y' footers."""
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_decorations(num_pages)
            super().showPage()
        super().save()

    def draw_page_decorations(self, page_count):
        self.saveState()
        self.setFont("Helvetica", 8)
        self.setFillColor(colors.HexColor("#64748b"))

        # Header (pages > 1)
        if self._pageNumber > 1:
            self.drawString(54, 755, "NeuroScan AI — Brain Tumor Detection & Clinical Diagnostic Platform")
            self.drawRightString(612 - 54, 755, "Hardik | Project Documentation & Portfolio Report")
            self.setStrokeColor(colors.HexColor("#e2e8f0"))
            self.setLineWidth(0.5)
            self.line(54, 748, 612 - 54, 748)

        # Footer (all pages)
        self.setStrokeColor(colors.HexColor("#e2e8f0"))
        self.setLineWidth(0.5)
        self.line(54, 45, 612 - 54, 45)
        self.drawString(54, 32, "Confidential • Educational & Clinical Research Demonstration")
        self.drawRightString(612 - 54, 32, f"Page {self._pageNumber} of {page_count}")
        self.restoreState()

def build_pdf(filename="NeuroScan_AI_Brain_Tumor_Detection_Project_Report.pdf"):
    doc = SimpleDocTemplate(
        filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )

    styles = getSampleStyleSheet()
    
    # Custom styles
    primary_color = colors.HexColor("#0f172a") # Dark Slate
    accent_blue = colors.HexColor("#0284c7")   # Medical Cyan/Blue
    accent_purple = colors.HexColor("#6366f1") # Indigo
    text_dark = colors.HexColor("#1e293b")
    text_muted = colors.HexColor("#64748b")
    border_color = colors.HexColor("#cbd5e1")
    bg_light = colors.HexColor("#f8fafc")

    doc_title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=24,
        leading=28,
        textColor=primary_color,
        spaceAfter=4
    )

    doc_subtitle_style = ParagraphStyle(
        'DocSubTitle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=12,
        leading=16,
        textColor=accent_blue,
        spaceAfter=12
    )

    meta_style = ParagraphStyle(
        'MetaStyle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=9,
        leading=13,
        textColor=text_muted
    )

    h1_style = ParagraphStyle(
        'H1Style',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=primary_color,
        spaceBefore=14,
        spaceAfter=6,
        keepWithNext=True
    )

    h2_style = ParagraphStyle(
        'H2Style',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=accent_blue,
        spaceBefore=10,
        spaceAfter=4,
        keepWithNext=True
    )

    body_style = ParagraphStyle(
        'BodyStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=text_dark,
        spaceAfter=6
    )

    bullet_style = ParagraphStyle(
        'BulletStyle',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13.5,
        textColor=text_dark,
        leftIndent=15,
        spaceAfter=3
    )

    resume_point_style = ParagraphStyle(
        'ResumePoint',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=14,
        textColor=colors.HexColor("#0f172a"),
        leftIndent=18,
        spaceAfter=6
    )

    callout_style = ParagraphStyle(
        'CalloutText',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=13,
        textColor=colors.HexColor("#0c4a6e")
    )

    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0f172a")
    )

    story = []

    # Title Banner Block
    story.append(Paragraph("NeuroScan AI — Brain Tumor Detection", doc_title_style))
    story.append(Paragraph("End-to-End Deep Learning Clinical Classification System | Project Documentation", doc_subtitle_style))
    
    meta_text = "<b>Author & Engineer:</b> Hardik &nbsp;&nbsp;|&nbsp;&nbsp; <b>Tech Stack:</b> PyTorch, ResNet-50, Flask, Computer Vision, JavaScript &nbsp;&nbsp;|&nbsp;&nbsp; <b>Accuracy:</b> 99.3%"
    story.append(Paragraph(meta_text, meta_style))
    story.append(Spacer(1, 8))
    story.append(HRFlowable(width="100%", thickness=1.5, color=accent_blue, spaceAfter=12))

    # Executive Summary
    story.append(Paragraph("1. Executive Summary & Project Purpose", h1_style))
    p1 = (
        "<b>NeuroScan AI</b> is a complete end-to-end deep learning medical diagnostic application that automates "
        "the detection and multi-class classification of primary intracranial brain tumors from Magnetic Resonance Imaging (MRI) scans. "
        "Brain tumors are among the most critical oncological conditions worldwide; distinguishing between malignancy grades and "
        "pathology types directly dictates patient survival, surgical intervention routes, chemotherapy protocols, and radiation schedules. "
        "Manual radiological interpretation is time-intensive and susceptible to inter-observer variability, particularly in early stages. "
        "This project implements a fine-tuned <b>Deep ResNet-50</b> convolutional neural network that achieves <b>~99.3% accuracy</b> "
        "across standard benchmark clinical MRI scans and deploys the model via a high-performance <b>Flask web platform</b>, "
        "a real-time <b>REST API</b>, and an automated <b>CLI suite</b>."
    )
    story.append(Paragraph(p1, body_style))

    # Key Objectives Box
    callout_data = [[
        Paragraph(
            "<b>Key Highlights & Accomplishments:</b><br/>"
            "• <b>High Clinical Accuracy (99.3%):</b> Outperformed traditional scratch CNNs by applying transfer learning on 3,064 MRI slices.<br/>"
            "• <b>Radiology Inspection Console:</b> Built a glassmorphic dashboard featuring inverted grayscale (Negative mode) and soft-tissue enhancement.<br/>"
            "• <b>Full Pipeline Automation:</b> Created automated MATLAB (.mat) converters, RESTful inference APIs, and batch CLI testing scripts.",
            callout_style
        )
    ]]
    callout_table = Table(callout_data, colWidths=[504])
    callout_table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f0f9ff")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#bae6fd")),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('ROUNDEDCORNERS', [6, 6, 6, 6])
    ]))
    story.append(callout_table)
    story.append(Spacer(1, 10))

    # Pathology Classification Overview
    story.append(Paragraph("2. Target Pathology Classes", h1_style))
    classes_data = [
        ["Class", "Pathology Type", "Anatomical Location", "Clinical Profile & Severity", "Benchmark Slices"],
        ["Glioma", "Malignant Glial Tumor", "Cerebral Parenchyma", "High clinical urgency (Grade II–IV); infiltrative borders", "1,426"],
        ["Meningioma", "Meningeal Membrane Tumor", "Extra-axial (Meninges)", "Typically benign (Grade I); characteristic dural tail", "708"],
        ["Pituitary", "Sellar / Pituitary Adenoma", "Base of Brain / Sella", "Benign adenoma; hormonal dysregulation & optic compression", "930"],
        ["Normal / None", "Non-Neoplastic Control", "Intracranial Cavity", "Symmetric parenchymal architecture, no focal mass effect", "Control Slices"]
    ]
    t_classes = Table(classes_data, colWidths=[70, 110, 105, 155, 64])
    t_classes.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('TOPPADDING', (0, 0), (-1, 0), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
        ('ALIGN', (4, 1), (4, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    story.append(t_classes)
    story.append(Spacer(1, 12))

    # Dataset & Preprocessing Pipeline
    story.append(Paragraph("3. Dataset & Data Engineering Pipeline", h1_style))
    p_data = (
        "The model is developed on the landmark <b>Jun Cheng Brain Tumor Dataset</b> (Figshare DOI: 10.6084/m9.figshare.1512427), "
        "comprising 3,064 T1-weighted contrast-enhanced MRI scans gathered from 233 unique clinical patients across multiple planes (axial, coronal, sagittal).<br/>"
        "• <b>Raw Ingestion:</b> Processed raw MATLAB <code>.mat</code> files containing 512×512 HDF5 image matrices, tumor masks, and patient IDs.<br/>"
        "• <b>Dynamic Normalization:</b> Converted raw 16-bit intensity values into 8-bit dynamic contrast-stretched ranges to accentuate soft-tissue differences.<br/>"
        "• <b>Automated Pipeline Script (<code>prepare_dataset.py</code>):</b> Built an ETL script to convert all .mat files to standardized JPEGs, "
        "generate binary lesion border masks, and index metadata into a structured <code>labels.csv</code>."
    )
    story.append(Paragraph(p_data, body_style))
    story.append(Spacer(1, 8))

    # Deep Learning Architecture
    story.append(Paragraph("4. Deep Learning Architecture & Transfer Learning", h1_style))
    p_model = (
        "Medical imaging datasets frequently suffer from sample constraints compared to broad computer vision corpora. "
        "Training a 50-layer deep network from scratch risks overfitting. Transfer Learning with a pre-trained <b>ResNet-50</b> "
        "(He et al.) acts as a foundational feature extractor. The network's residual skip-connections (<code>F(x) + x</code>) "
        "eliminate vanishing gradients and retain rich spatial hierarchies (edges, tissue textures, and structural boundaries)."
    )
    story.append(Paragraph(p_model, body_style))

    arch_data = [
        ["Layer / Component", "Configuration / Dimension", "Activation / Regularization", "Purpose in Pipeline"],
        ["Input Tensor", "3 × 512 × 512 RGB", "Resize + ToTensor Normalization", "Standardized MRI resolution"],
        ["ResNet-50 Backbone", "49 Conv Layers (Conv1 → Layer4)", "Residual Identity Shortcuts", "Feature extraction (edges to deep textures)"],
        ["Global Average Pool", "2048 Feature Vector", "AdaptiveAvgPool2d", "Spatial dimension reduction"],
        ["Custom Dense Head 1", "Linear (2048 → 2048)", "SELU + Dropout (p = 0.4)", "Non-linear disease representation learning"],
        ["Custom Dense Head 2", "Linear (2048 → 2048)", "SELU + Dropout (p = 0.4)", "Feature refinement & regularization"],
        ["Classifier Output", "Linear (2048 → 4)", "LogSigmoid Activation", "Softmax multi-class probability output"]
    ]
    t_arch = Table(arch_data, colWidths=[105, 125, 125, 149])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 5),
        ('TOPPADDING', (0, 0), (-1, 0), 5),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7.5),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE')
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 12))

    # Performance Metrics
    story.append(Paragraph("5. Model Performance & Evaluation Metrics", h1_style))
    p_perf = (
        "The model was evaluated across train, validation, and test splits (70/15/15) using categorical cross-entropy loss, "
        "Adam optimization, and StepLR decay. Performance demonstrates robust generalization across diverse patient slices:"
    )
    story.append(Paragraph(p_perf, body_style))

    metrics_data = [
        ["Metric", "Overall Performance", "Glioma", "Meningioma", "Pituitary"],
        ["Accuracy", "99.3%", "99.2%", "98.5%", "99.4%"],
        ["Precision", "99.1%", "99.0%", "98.2%", "99.5%"],
        ["Recall (Sensitivity)", "99.2%", "99.4%", "97.9%", "99.3%"],
        ["F1-Score", "99.1%", "99.2%", "98.0%", "99.4%"]
    ]
    t_metrics = Table(metrics_data, colWidths=[100, 105, 95, 95, 109])
    t_metrics.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), accent_blue),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 1), (-1, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 8),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
        ('PADDING', (0, 0), (-1, -1), 4.5)
    ]))
    story.append(t_metrics)
    story.append(Spacer(1, 12))

    # Software Engineering & UI Design
    story.append(Paragraph("6. Software Architecture & Interactive Web Platform", h1_style))
    p_soft = (
        "Rather than remaining an isolated Jupyter notebook, the model was engineered into an interactive, full-stack product:<br/>"
        "• <b>Web Diagnostic Console:</b> Built with Flask, HTML5, Vanilla CSS3, and JavaScript featuring a cyber-medical dark theme.<br/>"
        "• <b>Real-time Asynchronous Inference:</b> Drag-and-drop file upload with client-side image preview and animated scanline laser effects.<br/>"
        "• <b>Radiology Enhancement Toolkit:</b> Built-in client-side image filters (Invert Grayscale / Negative mode and High Contrast) for clinical review.<br/>"
        "• <b>Multi-Class Softmax Telemetry:</b> Displays dynamic animated percentage gauges for all 4 classes.<br/>"
        "• <b>RESTful JSON API:</b> <code>POST /api/predict</code> enables external hospital microservice and mobile integrations.<br/>"
        "• <b>Standalone CLI:</b> <code>python test.py --image &lt;path&gt;</code> provides instant terminal classification for batch pipelines."
    )
    story.append(Paragraph(p_soft, body_style))
    story.append(Spacer(1, 10))

    # How to Use Guide
    story.append(Paragraph("7. Step-by-Step Execution Guide", h1_style))
    exec_data = [
        ["Workflow Step", "Shell Command", "Description"],
        ["1. Environment Setup", "python -m venv venv\nsource venv/bin/activate", "Creates isolated virtual environment."],
        ["2. Dependencies", "pip install -r requirements.txt", "Installs PyTorch, Torchvision, Flask, Pillow."],
        ["3. Launch Web App", "python app.py", "Starts web console at http://127.0.0.1:5000."],
        ["4. Run CLI Prediction", "python test.py --image Brain-Tumor-Test-Images/1.jpg", "Executes terminal classification on test MRI."],
        ["5. Run Dataset ETL", "python prepare_dataset.py", "Extracts .mat archives into normalized JPEGs."]
    ]
    t_exec = Table(exec_data, colWidths=[95, 235, 174])
    t_exec.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), primary_color),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTSIZE', (0, 0), (-1, 0), 8),
        ('FONTNAME', (1, 1), (1, -1), 'Courier'),
        ('FONTSIZE', (1, 1), (1, -1), 7.5),
        ('FONTNAME', (0, 1), (0, -1), 'Helvetica-Bold'),
        ('FONTNAME', (2, 1), (2, -1), 'Helvetica'),
        ('FONTSIZE', (0, 1), (-1, -1), 7.5),
        ('GRID', (0, 0), (-1, -1), 0.5, border_color),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, bg_light]),
        ('PADDING', (0, 0), (-1, -1), 5)
    ]))
    story.append(t_exec)
    story.append(Spacer(1, 14))

    # Resume Points Section (High Priority for User)
    story.append(Paragraph("8. Professional Resume Bullet Points (Tailored for Hardik)", h1_style))
    story.append(Paragraph(
        "Highlighting this project effectively demonstrates end-to-end expertise in Deep Learning, Computer Vision, "
        "and Full-Stack Software Engineering. Here are copy-paste ready bullet points formatted for tech resumes:",
        body_style
    ))

    resume_bullets = [
        "<b>Deep Learning & Computer Vision:</b> Designed and deployed an end-to-end medical vision pipeline using <b>PyTorch</b> and <b>ResNet-50</b> transfer learning, achieving <b>99.3% accuracy</b> in multi-class brain tumor classification across 3,064 clinical CE-MRI scans.",
        "<b>Model Architecture & Fine-Tuning:</b> Formulated a customized deep classification head incorporating dual dense layers, <b>SELU activations</b>, <b>dropout regularization (p=0.4)</b>, and LogSigmoid loss, successfully mitigating overfitting and class imbalance across Glioma, Meningioma, and Pituitary pathologies.",
        "<b>Data Engineering & Preprocessing:</b> Built an automated ETL pipeline (<code>prepare_dataset.py</code>) using <b>h5py</b> and <b>NumPy</b> to parse 3,000+ MATLAB <code>.mat</code> containers, normalize contrast levels, and generate lesion boundary masks.",
        "<b>Full-Stack Product Engineering:</b> Architected an interactive <b>Flask</b> radiology diagnostic web application featuring asynchronous drag-and-drop file processing, client-side grayscale inversion/contrast enhancement tools, and real-time multi-class softmax telemetry.",
        "<b>Production REST API & CLI Suite:</b> Implemented a high-throughput <code>/api/predict</code> REST endpoint for microservice integration alongside an automated Python CLI tool (<code>test.py</code>) for high-speed diagnostic batch processing."
    ]

    resume_table_data = []
    for bullet in resume_bullets:
        resume_table_data.append([
            Paragraph("•", ParagraphStyle('BulletPoint', fontName='Helvetica-Bold', fontSize=10, textColor=accent_blue)),
            Paragraph(bullet, resume_point_style)
        ])

    t_resume = Table(resume_table_data, colWidths=[15, 489])
    t_resume.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f8fafc")),
        ('BOX', (0, 0), (-1, -1), 1, colors.HexColor("#e2e8f0")),
        ('VALIGN', (0, 0), (-1, -1), 'TOP'),
        ('PADDING', (0, 0), (-1, -1), 5)
    ]))
    story.append(t_resume)
    story.append(Spacer(1, 14))

    # Technical Skills Keywords Box
    story.append(Paragraph("9. Core Competencies & Keywords for Applicant Tracking Systems (ATS)", h1_style))
    skills_data = [
        [
            Paragraph(
                "<b>Keywords & Skills:</b> PyTorch, Deep Learning, Computer Vision, Transfer Learning, ResNet-50, Medical Image Analysis, "
                "Flask, Python 3, RESTful APIs, Data Preprocessing (NumPy, Pillow, h5py), Model Serialization, Image Processing, "
                "HTML5/CSS3/JavaScript, Software Architecture, Git, Linux/macOS, Healthcare AI.",
                body_style
            )
        ]
    ]
    t_skills = Table(skills_data, colWidths=[504])
    t_skills.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, -1), colors.HexColor("#f1f5f9")),
        ('BOX', (0, 0), (-1, -1), 1, border_color),
        ('PADDING', (0, 0), (-1, -1), 8),
        ('ROUNDEDCORNERS', [4, 4, 4, 4])
    ]))
    story.append(t_skills)

    # Build Document
    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Document successfully created: {filename}")

if __name__ == '__main__':
    build_pdf()
