## How to Setup and Run the Application

### 1. Clone the Repository
```bash
git clone https://github.com/onyevyerov/solar_panel_calculator
cd solar_panel_calculator
```
### 2. Set up the Virtual Environment
```
# Create (for all systems)
python -m venv venv

# Activation (Linux/macOS)
source venv/bin/activate

# Activation (Windows)
.\venv\Scripts\activate
```
### 3. Install Dependencies
```bash
pip install pytest
```
### 4. Customizing the Input File Path (Modifying `main.py`)

To run the calculation using your own data file, you must modify the path string within the `load_panels_from_file` call inside the `main()` function in `main.py`.

By default, the path is set to `"examples/sample_input.json"`.

```python
# In main.py (inside the main() function)
def main() -> None:
    # ----------------------------------------------------------------------------------
    # CHANGE THIS PATH to point to your custom data file (e.g., "my_data/custom.json")
    panels = load_panels_from_file("examples/sample_input.json")
    # ----------------------------------------------------------------------------------
    
    result = SolarPanelCalculator(panels).calculate()
    print(result)
```

### 5. Running the Application
Execute the main.py file from the root directory after setting your desired input path:
```bash
python main.py
```

### 6. How to Execute the Test Suite to Verify the Results
To verify the correctness and structural integrity of the calculation logic, run the test suite using pytest.
```bash
pytest
```