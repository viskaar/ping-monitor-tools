# Ping Monitor Tools 🚀

Python tools for network ping monitoring and analysis in DevAsc Linux environments.

## 📋 Features

### 1. Basic Ping Monitor (`src/ping_monitor.py`)
- Single target ping monitoring
- Detailed statistics and quality indicators
- Customizable ping count

### 2. Real-time Monitor (`src/ping_realtime.py`)  
- Continuous live monitoring
- Real-time visual progress bars
- Background execution

### 3. Multi-Target Comparator (`src/ping_compare.py`)
- Compare multiple targets simultaneously
- Performance ranking
- Custom target management

## 🚀 Usage

```bash
# Basic ping monitoring
python3 src/ping_monitor.py

# Real-time monitoring
python3 src/ping_realtime.py

# Multi-target comparison
python3 src/ping_compare.py

📊 Quality Indicators
💚 Excellent: < 50ms

💛 Good: 50-100ms

🟡 Fair: 100-200ms

🟠 Poor: 200-500ms

🔴 Very Poor: > 500ms

📝 Requirements
Python 3.6+

Linux environment

ping command access

🤝 Contributing


4. Commit message: `"Update README with usage instructions"`
5. Klik **"Commit changes"**

## Step 4: Buat Folder dan File Lainnya

### Buat Folder `examples`
1. **"Add file"** → **"Create new file"**
2. Nama file: `examples/basic_usage.py`
3. Isi dengan:

```python
#!/usr/bin/env python3
"""
Example: Basic usage of ping monitor tools
"""

print("Ping Monitor Tools - Examples")
print("Run the main programs from src/ directory")
