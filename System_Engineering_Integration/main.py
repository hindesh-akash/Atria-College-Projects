# Digital Twin for Sustainable Building System Integration

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime, timedelta
import json
import warnings
warnings.filterwarnings('ignore')

# Set up plotting style
plt.style.use('seaborn-v0_8')
sns.set_palette("husl")

class SensorData:
    """Class to simulate and manage sensor data"""
    
    def __init__(self):
        self.temperature_sensors = {}
        self.humidity_sensors = {}
        self.light_sensors = {}
        self.energy_meters = {}
        self.occupancy_sensors = {}
    
    def generate_realistic_data(self, hours=24*7):  # One week of data
        """Generate realistic sensor data for a week"""
        timestamps = [datetime.now() - timedelta(hours=i) for i in range(hours, 0, -1)]
        
        # Temperature data (°C) - varies with time of day
        base_temp = 25
        temp_variation = [base_temp + 5*np.sin(2*np.pi*i/24) + np.random.normal(0, 1) 
                         for i in range(hours)]
        
        # Humidity data (%) - inversely related to temperature
        humidity_data = [60 - (temp - base_temp) + np.random.normal(0, 3) 
                        for temp in temp_variation]
        
        # Light sensor data (lux) - daylight pattern
        light_data = [max(0, 800*np.sin(np.pi*i/12) + np.random.normal(0, 50)) 
                     if i % 24 < 12 else np.random.normal(10, 5) 
                     for i in range(hours)]
        
        # Energy consumption (kW) - varies with occupancy and HVAC usage
        energy_data = [2 + 3*np.sin(2*np.pi*i/24) + np.random.normal(0, 0.5) 
                      for i in range(hours)]
        
        # Occupancy (number of people) - office hours pattern
        occupancy_data = [max(0, int(20*np.sin(np.pi*(i%24)/12))) if 8 <= i%24 <= 18 
                         else np.random.poisson(2) for i in range(hours)]
        
        return pd.DataFrame({
            'timestamp': timestamps,
            'temperature': temp_variation,
            'humidity': humidity_data,
            'light_level': light_data,
            'energy_consumption': energy_data,
            'occupancy': occupancy_data
        })

class HVACSystem:
    """HVAC System simulation"""
    
    def __init__(self):
        self.target_temp = 24  # °C
        self.efficiency = 0.85
        self.power_rating = 50  # kW
        self.status = "AUTO"
        
    def calculate_load(self, current_temp, occupancy, external_temp=30):
        """Calculate HVAC load based on conditions"""
        temp_diff = abs(current_temp - self.target_temp)
        occupancy_load = occupancy * 0.1  # kW per person
        external_load = (external_temp - self.target_temp) * 0.05
        
        total_load = (temp_diff * 2 + occupancy_load + external_load) / self.efficiency
        return min(total_load, self.power_rating)
    
    def optimize_settings(self, forecast_data):
        """Optimize HVAC settings based on forecast"""
        recommendations = []
        for _, row in forecast_data.iterrows():
            if row['occupancy'] == 0:
                rec_temp = self.target_temp + 2  # Energy saving when unoccupied
            else:
                rec_temp = self.target_temp
            
            recommendations.append({
                'timestamp': row['timestamp'],
                'recommended_temp': rec_temp,
                'predicted_load': self.calculate_load(row['temperature'], row['occupancy'])
            })
        
        return pd.DataFrame(recommendations)

class LightingSystem:
    """Smart Lighting System simulation"""
    
    def __init__(self):
        self.fixtures = 100  # Number of LED fixtures
        self.power_per_fixture = 0.04  # kW per fixture
        self.daylight_threshold = 300  # lux
        
    def calculate_lighting_need(self, ambient_light, occupancy):
        """Calculate required artificial lighting"""
        if occupancy == 0:
            return 0  # Lights off when unoccupied
        
        if ambient_light < self.daylight_threshold:
            dimming_factor = 1 - (ambient_light / self.daylight_threshold)
            return self.fixtures * self.power_per_fixture * dimming_factor
        else:
            return 0  # Sufficient daylight
    
    def energy_consumption(self, sensor_data):
        """Calculate lighting energy consumption"""
        consumption = []
        for _, row in sensor_data.iterrows():
            power = self.calculate_lighting_need(row['light_level'], row['occupancy'])
            consumption.append(power)
        
        return consumption

class SolarPVSystem:
    """Solar PV System simulation"""
    
    def __init__(self):
        self.capacity = 100  # kW peak capacity
        self.efficiency = 0.18
        self.area = 500  # m²
        
    def calculate_generation(self, light_data, weather_factor=0.9):
        """Calculate solar power generation"""
        generation = []
        for light_level in light_data:
            # Convert lux to approximate solar irradiance (W/m²)
            irradiance = min(light_level * 0.1, 1000)  # Cap at 1000 W/m²
            
            power = (irradiance / 1000) * self.capacity * weather_factor
            generation.append(max(0, power))
        
        return generation

class BuildingEnergyManagement:
    """Building Energy Management System (BEMS)"""
    
    def __init__(self):
        self.hvac = HVACSystem()
        self.lighting = LightingSystem()
        self.solar = SolarPVSystem()
        self.grid_connection = True
        
    def calculate_energy_balance(self, sensor_data):
        """Calculate overall energy balance"""
        # Energy consumption
        hvac_consumption = [self.hvac.calculate_load(row['temperature'], row['occupancy']) 
                           for _, row in sensor_data.iterrows()]
        
        lighting_consumption = self.lighting.energy_consumption(sensor_data)
        
        # Base load (elevators, computers, etc.)
        base_load = [3 + np.random.normal(0, 0.2) for _ in range(len(sensor_data))]
        
        # Solar generation
        solar_generation = self.solar.calculate_generation(sensor_data['light_level'])
        
        # Calculate net energy
        total_consumption = np.array(hvac_consumption) + np.array(lighting_consumption) + np.array(base_load)
        net_energy = total_consumption - np.array(solar_generation)
        
        return pd.DataFrame({
            'timestamp': sensor_data['timestamp'],
            'hvac_consumption': hvac_consumption,
            'lighting_consumption': lighting_consumption,
            'base_load': base_load,
            'solar_generation': solar_generation,
            'total_consumption': total_consumption,
            'net_energy': net_energy,
            'grid_import': np.maximum(net_energy, 0),
            'grid_export': np.maximum(-net_energy, 0)
        })

class SustainabilityAssessment:
    """Sustainability and compliance assessment"""
    
    def __init__(self):
        # ECBC and GRIHA compliance parameters
        self.ecbc_epi_limit = 200  # kWh/m²/year for office buildings
        self.building_area = 5000  # m²
        self.emission_factor = 0.82  # kg CO2/kWh (India grid factor)
        
    def calculate_epi(self, annual_consumption):
        """Calculate Energy Performance Index (EPI)"""
        return annual_consumption / self.building_area
    
    def assess_ecbc_compliance(self, energy_data):
        """Assess ECBC compliance"""
        # Extrapolate weekly data to annual
        weekly_consumption = energy_data['total_consumption'].sum()
        annual_consumption = weekly_consumption * 52  # 52 weeks
        
        epi = self.calculate_epi(annual_consumption)
        compliance = epi <= self.ecbc_epi_limit
        
        return {
            'annual_consumption_kwh': annual_consumption,
            'epi_kwh_m2_year': epi,
            'ecbc_limit': self.ecbc_epi_limit,
            'compliance': compliance,
            'savings_potential': max(0, epi - self.ecbc_epi_limit) * self.building_area
        }
    
    def calculate_carbon_footprint(self, energy_data):
        """Calculate carbon footprint"""
        net_emissions = energy_data['grid_import'].sum() * self.emission_factor
        carbon_offset = energy_data['grid_export'].sum() * self.emission_factor
        
        return {
            'gross_emissions_kg_co2': net_emissions,
            'carbon_offset_kg_co2': carbon_offset,
            'net_emissions_kg_co2': net_emissions - carbon_offset,
            'annual_net_emissions_tonnes': (net_emissions - carbon_offset) * 52 / 1000
        }

class DigitalTwin:
    """Main Digital Twin class integrating all systems"""
    
    def __init__(self):
        self.sensors = SensorData()
        self.bems = BuildingEnergyManagement()
        self.sustainability = SustainabilityAssessment()
        self.data_history = []
        
    def run_simulation(self, hours=24*7):
        """Run the digital twin simulation"""
        print("🏢 Initializing Digital Twin for Sustainable Building...")
        print("=" * 60)
        
        # Generate sensor data
        print("📊 Generating sensor data...")
        sensor_data = self.sensors.generate_realistic_data(hours)
        
        # Calculate energy systems
        print("⚡ Calculating energy systems performance...")
        energy_data = self.bems.calculate_energy_balance(sensor_data)
        
        # Combine all data
        combined_data = pd.merge(sensor_data, energy_data, on='timestamp')
        
        # Sustainability assessment
        print("🌱 Performing sustainability assessment...")
        ecbc_assessment = self.sustainability.assess_ecbc_compliance(energy_data)
        carbon_assessment = self.sustainability.calculate_carbon_footprint(energy_data)
        
        # Store results
        self.data_history.append(combined_data)
        
        return combined_data, ecbc_assessment, carbon_assessment
    
    def visualize_results(self, data, ecbc_assessment, carbon_assessment):
        """Create comprehensive visualizations"""
        fig, axes = plt.subplots(3, 2, figsize=(15, 12))
        fig.suptitle('Digital Twin - Sustainable Building Performance Dashboard', fontsize=16, fontweight='bold')
        
        # Temperature and Occupancy
        ax1 = axes[0, 0]
        ax1_twin = ax1.twinx()
        ax1.plot(data['timestamp'], data['temperature'], 'r-', label='Temperature (°C)', linewidth=2)
        ax1_twin.bar(data['timestamp'], data['occupancy'], alpha=0.3, color='blue', label='Occupancy')
        ax1.set_ylabel('Temperature (°C)', color='red')
        ax1_twin.set_ylabel('Occupancy (persons)', color='blue')
        ax1.set_title('Environmental Conditions')
        ax1.tick_params(axis='x', rotation=45)
        
        # Energy Consumption Breakdown
        ax2 = axes[0, 1]
        energy_components = ['hvac_consumption', 'lighting_consumption', 'base_load']
        energy_values = [data[comp].mean() for comp in energy_components]
        colors = ['orange', 'yellow', 'green']
        ax2.pie(energy_values, labels=['HVAC', 'Lighting', 'Base Load'], colors=colors, autopct='%1.1f%%')
        ax2.set_title('Average Energy Consumption Breakdown')
        
        # Solar Generation vs Total Consumption
        ax3 = axes[1, 0]
        ax3.plot(data['timestamp'], data['total_consumption'], 'r-', label='Total Consumption', linewidth=2)
        ax3.plot(data['timestamp'], data['solar_generation'], 'g-', label='Solar Generation', linewidth=2)
        ax3.fill_between(data['timestamp'], data['solar_generation'], alpha=0.3, color='green')
        ax3.set_ylabel('Power (kW)')
        ax3.set_title('Energy Generation vs Consumption')
        ax3.legend()
        ax3.tick_params(axis='x', rotation=45)
        
        # Grid Import/Export
        ax4 = axes[1, 1]
        ax4.plot(data['timestamp'], data['grid_import'], 'r-', label='Grid Import', linewidth=2)
        ax4.plot(data['timestamp'], -data['grid_export'], 'g-', label='Grid Export', linewidth=2)
        ax4.axhline(y=0, color='black', linestyle='--', alpha=0.5)
        ax4.set_ylabel('Power (kW)')
        ax4.set_title('Grid Energy Exchange')
        ax4.legend()
        ax4.tick_params(axis='x', rotation=45)
        
        # ECBC Compliance
        ax5 = axes[2, 0]
        epi_current = ecbc_assessment['epi_kwh_m2_year']
        epi_limit = ecbc_assessment['ecbc_limit']
        bars = ax5.bar(['Current EPI', 'ECBC Limit'], [epi_current, epi_limit], 
                      color=['red' if epi_current > epi_limit else 'green', 'blue'])
        ax5.set_ylabel('EPI (kWh/m²/year)')
        ax5.set_title('ECBC Compliance Assessment')
        
        # Add compliance text
        compliance_text = "COMPLIANT" if ecbc_assessment['compliance'] else "NON-COMPLIANT"
        ax5.text(0.5, max(epi_current, epi_limit) * 0.8, compliance_text, 
                ha='center', va='center', fontweight='bold', fontsize=12,
                color='green' if ecbc_assessment['compliance'] else 'red')
        
        # Carbon Footprint
        ax6 = axes[2, 1]
        carbon_data = ['Gross Emissions', 'Carbon Offset', 'Net Emissions']
        carbon_values = [carbon_assessment['gross_emissions_kg_co2'], 
                        -carbon_assessment['carbon_offset_kg_co2'],
                        carbon_assessment['net_emissions_kg_co2']]
        colors = ['red', 'green', 'orange']
        bars = ax6.bar(carbon_data, carbon_values, color=colors)
        ax6.set_ylabel('CO₂ Emissions (kg/week)')
        ax6.set_title('Carbon Footprint Analysis')
        ax6.tick_params(axis='x', rotation=45)
        
        plt.tight_layout()
        plt.show()
        
        return fig
    
    def generate_report_summary(self, ecbc_assessment, carbon_assessment):
        """Generate performance summary report"""
        print("\n" + "="*80)
        print("🏢 DIGITAL TWIN PERFORMANCE SUMMARY REPORT")
        print("="*80)
        
        print(f"\n📊 ENERGY PERFORMANCE:")
        print(f"   • Annual Energy Consumption: {ecbc_assessment['annual_consumption_kwh']:,.0f} kWh")
        print(f"   • Energy Performance Index (EPI): {ecbc_assessment['epi_kwh_m2_year']:.1f} kWh/m²/year")
        print(f"   • ECBC Limit: {ecbc_assessment['ecbc_limit']} kWh/m²/year")
        print(f"   • ECBC Compliance: {'✅ COMPLIANT' if ecbc_assessment['compliance'] else '❌ NON-COMPLIANT'}")
        
        if not ecbc_assessment['compliance']:
            print(f"   • Required Energy Savings: {ecbc_assessment['savings_potential']:,.0f} kWh/year")
        
        print(f"\n🌱 SUSTAINABILITY METRICS:")
        print(f"   • Annual Net CO₂ Emissions: {carbon_assessment['annual_net_emissions_tonnes']:.1f} tonnes")
        print(f"   • Weekly Carbon Offset: {carbon_assessment['carbon_offset_kg_co2']:.1f} kg CO₂")
        print(f"   • Carbon Reduction vs Grid: {(carbon_assessment['carbon_offset_kg_co2']/carbon_assessment['gross_emissions_kg_co2']*100):.1f}%")
        
        print(f"\n🎯 GRIHA CONTRIBUTIONS:")
        print(f"   • Renewable Energy Integration: Solar PV system contributing to energy offset")
        print(f"   • Energy Efficient Systems: Optimized HVAC and smart lighting")
        print(f"   • Real-time Monitoring: IoT sensor integration for performance tracking")
        
        print(f"\n💡 OPTIMIZATION RECOMMENDATIONS:")
        if not ecbc_assessment['compliance']:
            print(f"   • Increase solar capacity or improve system efficiency")
            print(f"   • Implement advanced occupancy-based controls")
        print(f"   • Consider energy storage for peak shaving")
        print(f"   • Implement predictive maintenance protocols")
        
        print("="*80)

# Main execution
if __name__ == "__main__":
    # Initialize and run the Digital Twin
    dt = DigitalTwin()
    
    # Run simulation for one week
    print("🚀 Starting Digital Twin Simulation...")
    data, ecbc_results, carbon_results = dt.run_simulation(hours=24*7)
    
    # Visualize results
    print("📈 Generating visualizations...")
    dt.visualize_results(data, ecbc_results, carbon_results)
    
    # Generate comprehensive report
    dt.generate_report_summary(ecbc_results, carbon_results)
    
    # Export data for further analysis
    print("\n💾 Exporting data...")
    data.to_csv('digital_twin_building_data.csv', index=False)
    
    # Performance metrics over time
    print("\n📋 Key Performance Indicators (KPIs):")
    print(f"Average Energy Efficiency: {(data['solar_generation'].sum()/data['total_consumption'].sum()*100):.1f}% renewable")
    print(f"Peak Demand: {data['total_consumption'].max():.1f} kW")
    print(f"Load Factor: {(data['total_consumption'].mean()/data['total_consumption'].max()):.2f}")
    print(f"Solar Utilization: {(data['solar_generation'].mean()):.1f} kW average generation")
    
    print("\n✅ Digital Twin simulation completed successfully!")
    print("📄 Data exported to 'digital_twin_building_data.csv'")
    print("🎯 Ready for professional presentation and further analysis!")
