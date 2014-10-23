function reform_ds(cachedir)
% grigoris, 30/9: This function reforms the bounding boxes returned from
% DPM. DPM returns several bounding boxes as an outcome. However, we have
% spatial restrictions for the images, which we impose here. 
% In the end, one bbox is returned/saved per image, if the spatial
% restrictions are met. 

if nargin<1
    conf = voc_config();
    cachedir = conf.paths.model_dir;
end
load([cachedir 'mouth_train']); pos_m=pos; 
load([cachedir 'nose_train']); pos_n=pos; 

% fix the position of the nose 
[m_x_n,m_y_n] = compute_mean_bbox(pos_n);
load([cachedir 'nose_boxes']);
ds_n=fix_part(ds,m_x_n,m_y_n); 

% fix the position of the mouth 
load([cachedir 'mouth_boxes']);
[m_x_m,m_y_m] = compute_mean_bbox(pos_m);
ds_m=fix_part(ds,m_x_m,m_y_m); 

save([cachedir 'unified_boxes'],'ds_m','ds_n');

end

function [mean_x,mean_y] = compute_mean_bbox(pos)
% mean point of the positive bounding boxes
mean_x = 0; mean_y = 0;
for i=1:length(pos)
    bb      = pos(i).boxes;
    mean_x  = mean_x+(bb(1)+bb(3))/2;
    mean_y  = mean_y+(bb(2)+bb(4))/2;
end
mean_x      = mean_x/length(pos);
mean_y      = mean_y/length(pos);
end



function ds2=fix_part(ds,mean_x,mean_y)
ds2=cell(1,length(ds));
for i=1:length(ds)
    if ~isempty(ds{1,i})
        if size(ds{1,i},1)==1, ds2{1,i}=ds{1,i}; continue; end;
        j=0; found=false;
        while (j<size(ds{1,i},1))&&(~found)             % check if the mean point of bbox (from training data) is in some ds bbox
            j=j+1;  bb=ds{1,i}(j,:); 
            mx = (bb(1)+bb(3))/2;   my = (bb(2)+bb(4))/2;
            found = (bb(1)<=mean_x) && (bb(3)>mean_x) && (bb(2)<=mean_y) && (bb(4)>mean_y) ...
                    && abs(mean_x-mx)<8 && abs(mean_y-my)<8; % if yes, this is the bbox we save
        end
        if found 
           ds2{1,i} =  ds{1,i}(j,:);
        else                                            % if not, we find the one with the minimum euclidean distance from the middle
%             closest=100;  dist =1000000; 
%             for j=1:size(ds{1,i},1)
%                 bb=ds{1,i}(j,:); 
%                 mx = (bb(1)+bb(3))/2;   my = (bb(2)+bb(4))/2;
%                 dist2 = (mean_x-mx)^2+(mean_y-my)^2;
%                 if dist2<dist 
%                     closest=j; dist=dist2;
%                 end
%             end
%             ds2{1,i} =  ds{1,i}(closest,:);
        end
    end
end
end
