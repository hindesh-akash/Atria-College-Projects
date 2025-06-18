# Energy-System

## Techno-Economic and Policy Analysis of Solar-Battery Microgrid for Rural Electrification in India

### 📋 Project Overview

This repository contains a comprehensive analysis framework for designing, simulating, and evaluating decentralized solar-battery microgrid systems for village electrification in India. The project focuses on technical feasibility, economic viability, and policy alignment to provide sustainable energy solutions for rural communities.

### 🎯 Objectives

- Design optimal solar-battery microgrid systems for Indian villages
- Evaluate technical and economic feasibility
- Analyze policy alignment with government schemes
- Provide actionable insights for rural electrification projects

### 🔧 Key Features

#### Load Profiling
- Comprehensive load estimation for residential, educational, and agricultural sectors
- Hourly demand modeling for homes, schools, anganwadi centers, and irrigation systems
- Seasonal load variation analysis

#### Solar Resource Assessment
- Solar irradiance data analysis for optimal system sizing
- Monthly and daily solar resource evaluation
- Weather variation modeling

#### System Design & Optimization
- Automated PV capacity sizing based on energy demand
- Battery storage optimization with autonomy considerations
- Inverter sizing for peak load management
- Integration-ready for backup diesel generators

#### Economic Analysis
- CAPEX and OPEX calculations
- Levelized Cost of Electricity (LCOE) computation
- ROI and payback period analysis
- Subsidy modeling integration

#### Policy Integration
- Alignment with Saubhagya Scheme
- PM-KUSUM compatibility analysis
- Rural Electrification Scheme evaluation
- State-level incentive mapping

### 📊 Visualizations

The analysis generates 9 comprehensive plots:

1. **Daily Load Profile** - Hourly energy demand patterns
2. **Load Components Breakdown** - Sectoral energy consumption
3. **Solar Irradiance Analysis** - Resource availability assessment
4. **Monthly Solar Variations** - Seasonal resource mapping
5. **System Sizing Results** - Component capacity optimization
6. **Cost Breakdown Analysis** - Financial component distribution
7. **Energy Balance** - Supply-demand matching
8. **Seasonal Load Variations** - Annual demand fluctuations
9. **Financial Metrics** - Economic performance indicators

### 🚀 Getting Started

#### Prerequisites
```bash
pip install numpy pandas matplotlib seaborn
```

#### Installation
```bash
git clone https://github.com/yourusername/Energy-System.git
cd Energy-System
```

#### Usage
```python
# Run the main analysis
python solar_microgrid_analysis.py

# Or use in Jupyter Notebook
jupyter notebook solar_microgrid_analysis.ipynb
```

### 📈 Sample Results

**System Specifications:**
- PV Capacity: 15-20 kW
- Battery Capacity: 30-40 kWh  
- Inverter Capacity: 10-12 kW
- Daily Energy Demand: 15-20 kWh

**Economic Metrics:**
- CAPEX: ₹8-12 Lakhs
- LCOE: ₹6-8 per kWh
- Payback Period: 8-10 years
- IRR: 12-15%

### 🏛️ Policy Alignment

The system design considers:
- **Saubhagya Scheme**: Rural household electrification
- **PM-KUSUM**: Solar irrigation and grid integration
- **State Subsidies**: Renewable energy incentives
- **Net Metering**: Excess solar energy monetization

### 🔍 Key Insights

- Peak demand occurs during evening hours (18:00-20:00)
- Solar capacity utilization ranges 70-85%
- Battery autonomy provides 2-3 days backup
- LCOE competitive with grid electricity in rural areas
- Significant potential for carbon emission reduction

### 🛠️ Technical Specifications

**Modeling Approach:**
- Hourly time-step simulation
- Weather variability inclusion
- Component degradation modeling
- Grid integration capabilities

**Optimization Parameters:**
- Minimum LCOE targeting
- Reliability constraints (LPSP < 5%)
- Economic feasibility (IRR > 10%)
- Policy compliance requirements

### 📝 Future Enhancements

- [ ] Integration with HOMER Pro API
- [ ] Real-time weather data integration
- [ ] Machine learning for load forecasting
- [ ] Multi-village network optimization
- [ ] Advanced battery modeling (degradation)
- [ ] Smart grid connectivity features


### 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

### 👥 Authors

- **Hindesh Akash** - [YourGitHub](https://github.com/hindesh-akash)


### 📊 Project Status

🟢 **Active Development** - Regular updates and improvements

---

**Keywords:** Solar Energy, Microgrid, Rural Electrification, India, Renewable Energy, Battery Storage, LCOE, Techno-Economic Analysis, Policy Analysis, Energy Access
