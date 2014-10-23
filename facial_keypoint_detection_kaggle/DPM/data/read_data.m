function [pos, neg] = read_data(cls, M)
% grigoris, 30/9: This function extracts the annotated points from M and
% constructs the bounding boxes, which are saved in pos and neg structs. 

conf=voc_config(); 
cachedir   = conf.paths.model_dir;
numpos   = 0;
dataid   = 0;
numneg = 0;
try 
    load([cachedir cls '_train.mat']);
catch
    for id=1:size(M,1)
        flag1=false; 
        if strcmp(cls,'nose')
            bbox=round([M(id,17),min(M(id,18),M(id,14)),M(id,13),M(id,22)]); const=[-1,0,1,7]; % [x1,y1,x2,y2]
        elseif strcmp(cls,'mouth')
            bbox=round([M(id,25),M(id,28),M(id,23),M(id,30)]); const=[-2,0,2,0];
            if (bbox(2)>0)&&(bbox(4)>0)&&(bbox(4)-bbox(2)<5), const=[const(1),-4,const(3),4]; end
        elseif strcmp(cls,'eye_both')
            bbox=round([M(id,19),min([M(id,14),M(id,16),M(id,18),M(id,20)]),M(id,15),min(M(id,6),M(id,10))]); const=[0,-4,0,4];
        end
        
        if min(bbox)>0 && (bbox(4)-bbox(2)>0) && ( bbox(3)-bbox(1)>0)           % case when there is no missing element in the bbox
            flag1=true; bbox=bbox+const; bbox=[max(bbox(1),1),max(bbox(2),1),min(bbox(3),96),min(bbox(4),96)];
            numpos = numpos + 1; dataid = dataid + 1;
            pos(numpos,1) = pos_struct_creation(bbox,id,false,dataid);

            % Create flipped example
              numpos  = numpos + 1; dataid  = dataid + 1;
              oldx1   = bbox(1); oldx2   = bbox(3);
              bbox(1) = 96 - oldx2 + 1; bbox(3) = 96 - oldx1 + 1;
              pos(numpos,1) = pos_struct_creation(bbox,id,true,dataid);
        end

        if flag1 
            dataid             = dataid + 1;
            numneg             = numneg+1;
            neg(numneg,1).im = [id];
            neg(numneg,1).flip=false;
            neg(numneg,1).dataid=dataid;
            if strcmp(cls,'eyes')
                neg(numneg,1).pos_boxes=[pos(numpos-3,1).boxes;pos(numpos-1,1).boxes];
            else
                neg(numneg,1).pos_boxes=[pos(numpos-1,1).boxes];
            end
        end

    end
    save([cachedir cls '_train.mat'],'pos','neg');

end
end


function str = pos_struct_creation(bbox,id,flip,dataid)
str.im      = [id];
str.x1      = bbox(1);
str.y1      = bbox(2);
str.x2      = bbox(3);
str.y2      = bbox(4);
str.boxes   = bbox;
str.flip    = flip;
str.dataids = dataid;
str.sizes   = (bbox(3)-bbox(1)+1)*(bbox(4)-bbox(2)+1);
end

    