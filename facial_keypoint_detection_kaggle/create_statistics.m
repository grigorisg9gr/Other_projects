function create_statistics
% grigoris, 30/9: Creates statistics about the mean, variance of the training data points.
%
%
% Copyright (C) 2014 Grigorios Chrysos
% available under the terms of the Apache License, Version 2.0

fileN='data/training_allcomma.csv';
dtr=dlmread(fileN); % data_training
ft_cmp=create_comparison_feats;
feat_mat=dtr(:,1:30)';      % all feature points (for training)
diff_feat=zeros(size(feat_mat)); diff2_feat=zeros(size(feat_mat));
cnt_diff=zeros([1,size(feat_mat,1)]); cnt_diff2=cnt_diff;                  % counts how many non-zero elements in diff_feat
for featureNr=1:30
    if ft_cmp(featureNr,1)~=0
        for id=1:size(feat_mat,2)
            if (feat_mat(featureNr,id)~=0)&&(feat_mat(ft_cmp(featureNr,1),id)~=0)
                cnt_diff(featureNr)=cnt_diff(featureNr)+1;
                diff_feat(featureNr,cnt_diff(featureNr))=feat_mat(featureNr,id)-feat_mat(ft_cmp(featureNr,1),id);
            end
            if (ft_cmp(featureNr,2)~=0)&&(feat_mat(featureNr,id)~=0)&&(feat_mat(ft_cmp(featureNr,2),id)~=0)
                cnt_diff2(featureNr)=cnt_diff2(featureNr)+1;
                diff2_feat(featureNr,cnt_diff2(featureNr))=feat_mat(featureNr,id)-feat_mat(ft_cmp(featureNr,2),id);
            end
        end
    end
end

% now extract the mean differences and the std. Careful to ignore the zero
% elements in differences
cmp_mean=zeros([30,1]); cmp_std=cmp_mean; cmp_std2=cmp_mean; cmp_mean2=cmp_mean; mean_ft=cmp_mean; std_ft=cmp_mean;
for featureNr=1:30
    tmp_feat=feat_mat(featureNr,:);
    mean_ft(featureNr)=mean(tmp_feat(tmp_feat>0));
    std_ft(featureNr)=std(tmp_feat(tmp_feat>0));
    tmp_diff=diff_feat(featureNr,:);
    cmp_mean(featureNr)=mean(tmp_diff(tmp_diff~=0));
    cmp_std(featureNr)=std(tmp_diff(tmp_diff~=0));
    tmp_diff2=diff2_feat(featureNr,:);
    cmp_mean2(featureNr)=mean(tmp_diff2(tmp_diff2~=0),2);
    cmp_std2(featureNr)=std(tmp_diff2(tmp_diff2~=0));
end
cmp_std(isnan(cmp_std))=0;
cmp_std2(isnan(cmp_std2))=0;

% res=repmat(mean_ft,[1 size(dtr,1)]);
save data/statistics.mat
end


function ft_cmp=create_comparison_feats
% create an array to know which feats will be compared with which, eg 3 with 1
ft_cmp=zeros([30,2]);
ft_cmp(3:2:end,1)=1;  ft_cmp(4:2:end,1)=2;         % since most feats are compared with 1,2
ft_cmp([9,11,17,19,25],1)=3; ft_cmp([9,11,17,19,25]+1,1)=4;

ft_cmp(27,1)=21; ft_cmp(28,1)=22;
ft_cmp(29,1)=27; ft_cmp(30,1)=28;

ft_cmp(7,2)=5; ft_cmp(8,2)=6;
ft_cmp(11,2)=9; ft_cmp(12,2)=10;
ft_cmp(15,2)=13; ft_cmp(16,2)=14;
ft_cmp(19,2)=17; ft_cmp(20,2)=18;
ft_cmp(23,2)=21; ft_cmp(24,2)=22;
ft_cmp(25,2)=23; ft_cmp(26,2)=24;
end
