function bbox_to_face_feats(end_cachedir,split)
conf = voc_config();
cachedir = conf.paths.model_dir;
stats=0;
if nargin>0                             
    cachedir=[cachedir(1:end-1) end_cachedir];
    stats=1; split=num2str(split);
end
reform_ds(cachedir)
load([cachedir 'unified_boxes']); 
res=zeros([30, length(ds_n)]);
for i=1:length(ds_n)
    if ~isempty(ds_m{1,i})
        m_const=[2,0,-2,0];
        bbox=ds_m{1,i}(1:4)+m_const;
        res(25,i)=bbox(1);
    end
    if ~isempty(ds_n{1,i})
        n_const=[0,0,-2,-7];
        bbox=ds_n{1,i}(1:4)+n_const;
        res(17,i)=bbox(1); 
        res(13,i)=bbox(3);
        %heuristics:
        res(21,i)=(bbox(1)+bbox(3)+3)/2;                          % nose_tip_x will be in the middle of the bbox
    end
end

if stats,
    load(['../data/data_split' split]);             % cv set
    rmse=0; cnt=1;
    load('../data/statistics.mat');
    cmp_diff=zeros(size(res)); diff_mean_gt=zeros(size(res));
    for id=1:size(data_cv,1)
        for featureNr=1:30
            if data_cv(id,featureNr)~=0 && res(featureNr,id)~=0
                rmse=rmse+(res(featureNr,id)-data_cv(id,featureNr))^2;
                cnt=cnt+1;
                cmp_diff(featureNr,id)=res(featureNr,id)-data_cv(id,featureNr);
                diff_mean_gt(featureNr,id)=mean_ft(featureNr)-data_cv(id,featureNr);
            end
        end
    end
    rmse=sqrt(rmse/cnt-1)
    cmp_mean=zeros([30,1]); cmp_std=cmp_mean;
    for featureNr=1:30
        tmp_cmp=cmp_diff(featureNr,:);
        cmp_mean(featureNr)=mean(tmp_cmp(tmp_cmp>0));
        cmp_std(featureNr)=std(tmp_cmp(tmp_cmp>0));
    end
    save([cachedir 'stats.mat'],'rmse','cmp_std','cmp_mean','cmp_diff','diff_mean_gt');
else
    load('../data/statistics.mat');
    for id=1:length(ds_n)
        for featureNr=1:30
            if res(featureNr,id)>0, continue; end
            res(featureNr,id)=mean_ft(featureNr);
        end
    end
    save ../data/res.mat res
end

end


