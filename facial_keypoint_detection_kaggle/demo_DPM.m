% Copyright (C) 2014 Grigorios Chrysos
% available under the terms of the Apache License, Version 2.0

create_statistics() 

% Train the Deformable part models (http://www.cs.berkeley.edu/~rbg/latent/) for the nose and the mouth. 
% The training may require several hours depending on your machine. 
cd DPM/ ; startup; 
pascal('mouth',2);   
pascal('nose',1);

bbox_to_face_feats(); 

% format the final submission file with the required points. THe submission
% file will be saved in the data/ folder. 
cd ../
format_submission_file()
