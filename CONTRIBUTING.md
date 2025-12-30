# Contributing to the Pais Effect Demonstrator

Thank you for your interest in contributing! This is a community science project and we welcome all forms of participation.

## Ways to Contribute

### 🔧 Build and Test
The most valuable contribution is building the apparatus and sharing your results:

1. Follow the build documentation in `/docs/`
2. Execute the experimental protocols
3. Share your data and analysis (see below)

### 📊 Share Results
Whether positive or negative, your results are valuable:

1. Fork this repository
2. Create a branch: `results/your-name-date`
3. Add your data to `community-results/your-name/`
4. Include:
   - Raw data files (CSV)
   - Analysis outputs
   - Session logs
   - Photos of your setup (optional but helpful)
5. Submit a pull request

### 📝 Improve Documentation
- Fix typos or unclear instructions
- Add troubleshooting tips based on your experience
- Improve diagrams
- Translate to other languages

### 💻 Improve Software
- Enhance analysis scripts
- Add visualization tools
- Improve DAQ firmware
- Create calibration utilities

### 🔬 Propose Experiments
- Suggest additional control experiments
- Propose parameter variations
- Identify potential artifacts we haven't considered

## Code of Conduct

### Scientific Integrity
- Report results honestly, including null results
- Document methodology completely
- Acknowledge uncertainty
- Don't overstate conclusions

### Safety First
- Never compromise on safety procedures
- Report any safety incidents or near-misses
- Suggest safety improvements

### Respectful Collaboration
- Be constructive in feedback
- Respect different skill levels
- Help newcomers get started

## Submitting Changes

### For Documentation
1. Fork the repo
2. Create a feature branch
3. Make your changes
4. Submit a pull request with clear description

### For Code
1. Fork the repo
2. Create a feature branch
3. Follow existing code style
4. Test your changes
5. Submit a pull request

### For Results
1. Fork the repo
2. Create a results branch
3. Add your data with documentation
4. Submit a pull request

## Results Format

When sharing experimental results, please include:

```
community-results/
└── your-name-YYYYMMDD/
    ├── README.md           # Summary of your setup and findings
    ├── setup-photos/       # Photos of your apparatus
    ├── raw-data/           # Original CSV files from DAQ
    ├── analysis/           # Your analysis outputs
    ├── logs/               # Session logs
    └── conclusions.md      # Your interpretation
```

### README Template for Results

```markdown
# Results from [Your Name]

## Setup Summary
- **Date:** YYYY-MM-DD
- **Location:** [City, Country]
- **Apparatus Version:** [any modifications from standard]

## Key Parameters
- Piezo type: [commercial/DIY]
- Max frequency tested: X kHz
- Max voltage tested: X kV
- Magnetometer: [model]

## Summary of Results
[Brief description]

## Conclusions
[Your interpretation]

## Files Included
[List of data files]
```

## Questions?

- Open a GitHub Issue for technical questions
- Use Discussions for general questions
- Tag issues appropriately: `bug`, `enhancement`, `question`, `results`

## Recognition

All contributors will be acknowledged in the project README. Significant contributions (successful builds, novel analysis, etc.) will be highlighted.

---

*Remember: Null results are valuable! Don't be discouraged if you don't detect an anomaly - that's important scientific data.*
