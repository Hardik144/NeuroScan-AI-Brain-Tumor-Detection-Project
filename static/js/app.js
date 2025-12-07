// Brain Tumor Diagnostic Workspace Logic
document.addEventListener('DOMContentLoaded', () => {
  const dropzone = document.getElementById('dropzone');
  const fileInput = document.getElementById('file-input');
  const previewWrapper = document.getElementById('preview-wrapper');
  const mriPreviewImg = document.getElementById('mri-preview-img');
  const scanCanvas = document.getElementById('scan-canvas');
  const btnPredict = document.getElementById('btn-predict');
  const resultsEmpty = document.getElementById('results-empty');
  const resultsContent = document.getElementById('results-content');
  const toastMsg = document.getElementById('toast-msg');

  // Interactive Tools Elements
  const btnInvert = document.getElementById('tool-invert');
  const btnContrast = document.getElementById('tool-contrast');
  const btnResetTools = document.getElementById('tool-reset');
  const btnPrintReport = document.getElementById('btn-print-report');

  let currentFile = null;
  let isInverted = false;
  let isHighContrast = false;

  // Clinical information lookup dictionary
  const CLINICAL_INSIGHTS = {
    'Glioma': {
      colorClass: 'glioma',
      badge: 'High Clinical Priority',
      description: 'Gliomas are tumors that arise from glial cells (astrocytes, oligodendrocytes, and ependymal cells) in the brain or spinal cord. They represent the majority of malignant brain tumors.',
      findings: [
        'Often infiltrative with ill-defined hyperintense borders on T2/FLAIR scans.',
        'Immediate multidisciplinary neuro-oncology evaluation advised.',
        'Surgical resection, radiotherapy, and temozolomide chemotherapy standard protocols.'
      ]
    },
    'Meningioma': {
      colorClass: 'meningioma',
      badge: 'Intermediate Clinical Priority',
      description: 'Meningiomas arise from the meninges—the membranes that surround your brain and spinal cord. Most are benign (Grade I) and slow-growing, though they can exert pressure on brain tissue.',
      findings: [
        'Typically extra-axial, well-demarcated with characteristic "dural tail" enhancement.',
        'Management ranges from active MRI surveillance for small lesions to surgical resection.',
        'Stereotactic radiosurgery (Gamma Knife) effective for skull base locations.'
      ]
    },
    'Pitutary': {
      colorClass: 'pituitary',
      badge: 'Endocrine & Visual Assessment Needed',
      description: 'Pituitary adenomas originate in the pituitary gland at the base of the brain behind the nasal passage. Most are non-cancerous (benign) adenomas that can affect hormone balance or optic nerves.',
      findings: [
        'Sella turcica expansion with potential chiasmal compression (bitemporal hemianopsia).',
        'Formal endocrine blood panel (PRL, GH, ACTH, TSH) and visual field testing indicated.',
        'Transsphenoidal endoscopic resection or dopamine agonist therapy (for prolactinomas).'
      ]
    },
    'None': {
      colorClass: 'none',
      badge: 'No Significant Mass Detected',
      description: 'No clear radiographic signs of common intracranial neoplastic lesions identified in the examined region. Ventricles and parenchymal architecture appear within normal parameters.',
      findings: [
        'Symmetric cerebral hemispheres with preserved grey-white differentiation.',
        'No focal midline shift or mass effect observed.',
        'Correlate with patient symptoms; further dedicated volumetric sequences if symptoms persist.'
      ]
    }
  };

  // Toast helper
  function showToast(message) {
    toastMsg.textContent = message;
    toastMsg.classList.add('show');
    setTimeout(() => {
      toastMsg.classList.remove('show');
    }, 4000);
  }

  // File loading and preview
  function handleFile(file) {
    if (!file) return;
    if (!file.type.startsWith('image/')) {
      showToast('Please select a valid image file (PNG, JPG, JPEG).');
      return;
    }

    currentFile = file;
    const reader = new FileReader();
    reader.onload = (e) => {
      mriPreviewImg.src = e.target.result;
      previewWrapper.style.display = 'flex';
      btnPredict.disabled = false;
      resetImageFilters();

      // Smooth scroll to preview if on mobile
      if (window.innerWidth < 768) {
        previewWrapper.scrollIntoView({ behavior: 'smooth' });
      }
    };
    reader.readAsDataURL(file);
  }

  // Drag & Drop handlers
  dropzone.addEventListener('click', () => fileInput.click());

  dropzone.addEventListener('dragover', (e) => {
    e.preventDefault();
    dropzone.classList.add('dragover');
  });

  ['dragleave', 'dragend'].forEach(type => {
    dropzone.addEventListener(type, () => {
      dropzone.classList.remove('dragover');
    });
  });

  dropzone.addEventListener('drop', (e) => {
    e.preventDefault();
    dropzone.classList.remove('dragover');
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      handleFile(e.dataTransfer.files[0]);
    }
  });

  fileInput.addEventListener('change', (e) => {
    if (e.target.files && e.target.files.length > 0) {
      handleFile(e.target.files[0]);
    }
  });

  // Sample Scans loader
  document.querySelectorAll('.sample-btn').forEach(btn => {
    btn.addEventListener('click', async (e) => {
      const filename = btn.getAttribute('data-sample');
      try {
        btn.style.opacity = '0.5';
        const response = await fetch(`/api/sample/${filename}`);
        if (!response.ok) throw new Error('Could not fetch sample scan.');
        
        const blob = await response.blob();
        const file = new File([blob], filename, { type: blob.type || 'image/jpeg' });
        handleFile(file);
        showToast(`Loaded sample scan: ${filename}`);
      } catch (err) {
        showToast('Error loading sample image.');
      } finally {
        btn.style.opacity = '1';
      }
    });
  });

  // Image Viewer Tools (Radiology inspection filters)
  function updateImageFilters() {
    let filters = [];
    if (isInverted) filters.push('invert(100%)');
    if (isHighContrast) filters.push('contrast(180%) brightness(110%)');
    mriPreviewImg.style.filter = filters.length > 0 ? filters.join(' ') : 'none';
  }

  function resetImageFilters() {
    isInverted = false;
    isHighContrast = false;
    btnInvert.classList.remove('active');
    btnContrast.classList.remove('active');
    updateImageFilters();
  }

  btnInvert.addEventListener('click', () => {
    isInverted = !isInverted;
    btnInvert.classList.toggle('active', isInverted);
    updateImageFilters();
  });

  btnContrast.addEventListener('click', () => {
    isHighContrast = !isHighContrast;
    btnContrast.classList.toggle('active', isHighContrast);
    updateImageFilters();
  });

  btnResetTools.addEventListener('click', resetImageFilters);

  // Prediction analysis trigger
  btnPredict.addEventListener('click', async () => {
    if (!currentFile) {
      showToast('Please upload or select an MRI scan first.');
      return;
    }

    // Start scanner animation
    scanCanvas.classList.add('scanning');
    btnPredict.disabled = true;
    btnPredict.innerHTML = `
      <svg class="spinner" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
        <circle cx="12" cy="12" r="10" stroke-dasharray="32" stroke-linecap="round"></circle>
      </svg>
      Analyzing Neural Tensor...
    `;

    const formData = new FormData();
    formData.append('file', currentFile);

    try {
      const response = await fetch('/api/predict', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.error || 'Server error during prediction');
      }

      const data = await response.json();
      displayResults(data);
      showToast(`Analysis completed: ${data.class_name}`);
    } catch (err) {
      showToast(`Prediction failed: ${err.message}`);
    } finally {
      scanCanvas.classList.remove('scanning');
      btnPredict.disabled = false;
      btnPredict.innerHTML = `
        <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <path d="M12 2v4M12 18v4M4.93 4.93l2.83 2.83M16.24 16.24l2.83 2.83M2 12h4M18 12h4M4.93 19.07l2.83-2.83M16.24 7.76l2.83-2.83"/>
        </svg>
        Re-Analyze MRI Scan
      `;
    }
  });

  // Render prediction results to UI
  function displayResults(data) {
    const className = data.class_name;
    const confidence = data.confidence.toFixed(1);
    const probs = data.probabilities || {};

    const info = CLINICAL_INSIGHTS[className] || CLINICAL_INSIGHTS['None'];

    // Update Diagnosis Hero Card
    const diagnosisCard = document.getElementById('diagnosis-hero-card');
    diagnosisCard.className = `diagnosis-card ${info.colorClass}`;

    document.getElementById('diagnosis-badge').textContent = info.badge;
    document.getElementById('diagnosis-timestamp').textContent = new Date().toLocaleTimeString();
    document.getElementById('diagnosis-title').textContent = className === 'None' ? 'No Tumor Detected' : `${className} Tumor`;
    document.getElementById('confidence-number').textContent = `${confidence}%`;

    // Update Probability Bars
    const probClasses = [
      { key: 'Glioma', barId: 'bar-glioma', pctId: 'pct-glioma' },
      { key: 'Meningioma', barId: 'bar-meningioma', pctId: 'pct-meningioma' },
      { key: 'Pitutary', barId: 'bar-pituitary', pctId: 'pct-pituitary' },
      { key: 'None', barId: 'bar-none', pctId: 'pct-none' }
    ];

    probClasses.forEach(item => {
      const val = (probs[item.key] !== undefined) ? probs[item.key] : 0;
      const barEl = document.getElementById(item.barId);
      const pctEl = document.getElementById(item.pctId);
      if (barEl && pctEl) {
        barEl.style.width = `${Math.max(2, val.toFixed(1))}%`;
        pctEl.textContent = `${val.toFixed(1)}%`;
      }
    });

    // Update Clinical Insights
    document.getElementById('clinical-desc').textContent = info.description;
    const findingsList = document.getElementById('clinical-findings');
    findingsList.innerHTML = '';
    info.findings.forEach(f => {
      const li = document.createElement('li');
      li.textContent = f;
      findingsList.appendChild(li);
    });

    // Show results panel
    resultsEmpty.style.display = 'none';
    resultsContent.style.display = 'flex';

    if (window.innerWidth < 1080) {
      resultsContent.scrollIntoView({ behavior: 'smooth' });
    }
  }

  // Print Report
  if (btnPrintReport) {
    btnPrintReport.addEventListener('click', () => {
      window.print();
    });
  }
});
