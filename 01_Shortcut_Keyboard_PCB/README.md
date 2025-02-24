# PCB Documentation

KiCad project files for the Shortcut-Keyboard PCB based on RP2040.

## RP2040 Interface Block Diagram
Interface overview of the used RP2040 microcontroller pins and buses:

<p align="center">
  <img src="04_Pictures/RP2040 - System Block Diagram.svg" width="600">
  <br>
  <em>RP2040 Microcontroller Interface</em>
</p>

## Directory Structure

### Folders
- `01_Schematic/` - Schematic exports and documentation
- `02_BOM/` - Bill of Materials and part lists
- `03_STEP/` - 3D models and mechanical files

### KiCad Files
- `shortcut_keyboard.kicad_pro` - Project file
- `shortcut_keyboard.kicad_sch` - Main schematic
- `shortcut_keyboard.kicad_pcb` - PCB layout
- `MCU.kicad_sch` - MCU specific schematic
- `Connector.kicad_sch` - Connector specific schematic
- `Revision_History.kicad_sch` - Version tracking


## Layer Stackup
This PCB uses a SIG/GND/VCC/SIG stackup instead of the more conventional SIG/GND/GND/SIG configuration. This decision was based on several design considerations:

1. **Design Optimization:** The chosen stackup provides an optimal balance between routing efficiency and performance for this specific application.

2. **Signal Requirements Analysis:** After analyzing the signal integrity requirements for the RP2040-based keyboard, I determined that the modest-speed signals don't demand the theoretical advantages of dual ground planes.

3. **Power Distribution:** The dedicated VCC plane on L3 provides sufficient power distribution for all components while simplifying the overall routing strategy.

4. **Manufacturing Considerations:** The SIG/GND/VCC/SIG configuration maintains the same manufacturing complexity while offering adequate electrical performance for this application.

5. **Application-Specific Design:** For this particular keyboard application, the SIG/GND/VCC/SIG arrangement meets all functional requirements while enabling a more streamlined development process.


## Specifications
- Size: 100 x 79 mm
- Layers: 4 layer, 1.6mm FR4
- Version: V1.00.01 (2025-02-02)
- KiCad Version: 8.0.7
