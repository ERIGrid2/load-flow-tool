# Load-Flow-tool

This is an open source load flow tool developed by CRES (Evangelos Rikos) in Python within the framework of ERIGrid 2.0.

In order for the user to easily use the specific tool some guidelines are provided below:

-The tool consists of four (4) python files, the main LF tool as well as three functions for the construction and conversion of the Ybus matrix and for the calculation of the remaining operating availability/capacities of lines and voltage deviations from their nominal values.

-The tool uses a set of input data in *.txt form that through which the user can specify a large number of parameters of the grid. The Bus_location.txt specifies the bus type (0, 1, or 2) as well as its reactive power limits (in case of type a 2 bus). The Grid_data.txt provides the grid topology information, including number of line, buses between which the line is located as well as line parameters (R, X and Capacity). The Initial_voltages.txt file contains the initial estimation of the voltage values (Bus number, amplitude in pu, angle in rad and nominal voltage in kV). The Power_schedule2.txt contains information about the active and reactive power of the resources per timeframe. The sign convention is positive for power generation, negative for power consumption. An unique identification number (EAN) is used to specify which resource we are referring to. This is especially useful because the tool allows the user to specify for each node separate resources (generators, loads). The tool then aggregates the resources according to their connectivity which is specified by Resources_connectivity.txt. Last but not least, the user has to define the number and characteristics of transformers in the grid. In the Trasnformers.txt file the user defines the transformer number,its connection between buses (from HV to LV), the transformation ratio, the parameters (R and X) as well as its maximum capacity. If the grid does not contain any transformers the data values should be empty.

-There are some additional parameters within the load flow tool itself that the user has to select appropriately: 'numbuses' is the number of buses, 'timeframe' is used to select the specific timeframe from the power schedule, 'Zbase', 'Sbase' and 'Vbase' are the base values for Impedance, Apparent power and Voltage respectively. 

-There are some additional parameters in the input files that are not used in the current version such as the location of the buses in x-y coordinates. The scope of these coordinates is to be used in graphical illustration of the system in future versions of the tool.   

### Funding acknowledment

<img alt="European Flag" src="https://erigrid2.eu/wp-content/uploads/2020/03/europa_flag_low.jpg" align="left" style="margin-right: 10px"/> The development of Load-Flow-tool has been supported by the [ERIGrid 2.0](https://erigrid2.eu) project of the H2020 Programme under [Grant Agreement No. 870620](https://cordis.europa.eu/project/id/870620)
