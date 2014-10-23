function format_submission_file
% Formats the file in the form accepted in the competition. 
% It accepts one *.mat file with all the detected points per test image. 
% Then it compares it with the IdLookupTable.csv (from kaggle site) and fills a new csv with the required points. 
%
%
% Copyright (C) 2014 Grigorios Chrysos
% available under the terms of the Apache License, Version 2.0
fid = fopen('data/IdLookupTable.csv','r');
C = textscan(fid, repmat('%s',1,4), 'delimiter',',', 'CollectOutput',true);
C=C{1};
fclose(fid);
% features 
fid = fopen('data/features.csv','r');
feats = textscan(fid, repmat('%s',1,2), 'delimiter',',', 'CollectOutput',true);
feats=feats{1};
fclose(fid);
% our detection system
load data/res.mat
% final submission file
fileID = fopen('data/submission_nums.csv','w');


cnt=2;
for i=1:1783 % total test images
    cnt_feat=1;
    while (cnt<=size(C,1))&&(str2num(C{cnt,2})==i)
        cnt_feat=cnt_feat+1;
        if strcmp(feats{cnt_feat,2},C{cnt,3})==1        % then match the point
            C{cnt,4}=num2str(res(cnt_feat-1,i));
            cnt=cnt+1;
%         else
%             fprintf('Skipped\n');;
        end
    end
end

[nrows,ncols] = size(C);
for row = 1:nrows
fprintf(fileID,'%s,%s\n',C{row,1},C{row,4});
end
fprintf('Done\n');
end
