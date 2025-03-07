function triggerVibration(vibrationType, delayMs)
    % TRIGGERVIBRATION Triggers haptic feedback on SteelSeries Rival 700 mouse.
    %   triggerVibration(vibrationType, delayMs) sends a vibration command to the
    %   SteelSeries Rival 700 mouse with the specified vibration type and delay.
    %
    %   Inputs:
    %       vibrationType - String or number specifying the vibration pattern
    %                       (e.g., 'Buzz', 'Strong', or an integer 0-127).
    %       delayMs       - Numeric delay in milliseconds before the vibration.
    %
    %   Example:
    %       triggerVibration('Buzz', 250)  % Triggers Buzz pattern after 250ms
    %       triggerVibration(10, 100)      % Triggers custom vibration 10 after 100ms

    % Get the directory of this MATLAB script
    scriptPath = mfilename('fullpath');
    [pyScriptDir, ~, ~] = fileparts(scriptPath);  % Directory containing this .m file
    
    % Path to the Python script in the parent directory
    pyScript = fullfile(pyScriptDir, 'steelseries_vibration.py');
    
    % Validate script exists
    if ~exist(pyScript, 'file')
        error('Python script not found at: %s', pyScript);
    end
    
    % Validate and convert vibrationType to string
    if isnumeric(vibrationType)
        vibrationType = num2str(vibrationType);
    elseif ~ischar(vibrationType)
        error('vibrationType must be a string or numeric value');
    end
    
    % Validate and convert delayMs to integer
    if ~isnumeric(delayMs) || delayMs < 0
        error('delayMs must be a non-negative numeric value (in milliseconds)');
    end
    delayMs = int32(delayMs); % Python expects an integer
    
    % Call the Python function
    try
        % Add script directory to Python's sys.path
        py.sys.path().append(pyScriptDir);
        
        % Import the Python module
        pyModule = py.importlib.import_module('steelseries_vibration');
        
        % Call trigger_vibration with vibrationType and delayMs
        result = py.steelseries_vibration.trigger_vibration(vibrationType, delayMs);
        
        % Check result (True/False from Python)
        if result
            disp(['Vibration type "', vibrationType, '" triggered successfully after ', num2str(delayMs), 'ms']);
        else
            disp(['Failed to trigger vibration type "', vibrationType, '" with delay ', num2str(delayMs), 'ms']);
        end
    catch e
        disp('Error calling Python script:');
        disp(e.message);
    end
end
