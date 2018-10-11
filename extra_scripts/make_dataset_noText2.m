% 
% Label: valence and arousal
% Modify COGNIMUSE dataset to our own format
%  Multimodal dataset: audio, scene and emotion (NO TEXT)
%  By not considering subtitles, it allows us to segment the audio and movie into equal parts
% 
% Author: Gwena Cunha
% Date: June 29th 2018
%

%% Settings
root_path = 'DataWithEmotionTags_noText/';
segment_size = 3;  % in seconds

%Get subdirectories in root
dinfo = dir(root_path);
dinfo(ismember( {dinfo.name}, {'.', '..'})) = [];  %remove . and ..
dir_idxs = find(vertcat(dinfo.isdir));
subdirs = [];
for i=1:length(dir_idxs)
  subdirs = [subdirs, {dinfo(dir_idxs(i)).name}];
end

%% Load features from each directory
%i=1
for i=1:length(subdirs)
    path_video = strcat([root_path, subdirs{i}, '/'])

    % Emotion scores
    path_emotion = strcat(path_video, 'emotion/');
    fid = fopen(strcat(path_emotion, 'intended_1.dat'),'r');
    datacell = textscan(fid, '%f%f%f', 'Collect', 1); %'HeaderLines', 1
    fclose(fid);
    % Time: 0.04 means 4 seconds (we want it in the format of 4 seconds, not 0.4)
    emotion_scores = datacell{1};
    emotion_scores(:,1) = emotion_scores(:,1)*100;
    
    % Read subs txt file and get structure A with text
    path_video_files = strcat(path_video, 'video.mp4');
    
    % Video
    % Source: https://kr.mathworks.com/matlabcentral/answers/195330-how-to-play-video-at-specific-timestamp
    % create the object
    vidObj = VideoReader(path_video_files);
    % determine the number of frames per second
    fps = get(vidObj,'FrameRate')
    % determine the number of frames
    numFrames = get(vidObj,'NumberOfFrames')  % 56271
    
    % number of frames per segment_size
    fps_seg = floor(fps * segment_size)
    
    % Audio
    [y,Fs] = audioread(path_video_files);
    
    j=1;
    count=1;
    emotion_scores_matrix = [];
    emotion_scores_matrix_va = [];
    emotion_scores_matrix_va_raw = [];
    splice_count = 1;
    seconds_count = segment_size;
    for j=1:fps_seg:numFrames-fps_seg
        % Splice video according to sentences start and end times
        % read all data in a time period
        frame_start = j
        frame_end = min(j+fps_seg, numFrames-1)
        video = read(vidObj,[frame_start frame_end]);

        % Save splice i in Spliced Data dir
        new_path_video_files = strcat([path_video, 'splices_video/']);
        if exist(new_path_video_files,'dir') ~= 7
            mkdir(new_path_video_files);
        end
        splice_name = strcat([new_path_video_files, num2str(splice_count), '.avi']);
        v = VideoWriter(splice_name);
        open(v);
        writeVideo(v, video);
        close(v);
        
        % read splices to extract audio
        new_path_audio_files = strcat([path_video, 'splices_audio/']);
        if exist(new_path_audio_files,'dir') ~= 7
            mkdir(new_path_audio_files);
        end
        audio_filename = strcat([new_path_audio_files, num2str(splice_count), '.wav']);
        i_idx = max(1, min(floor(Fs*seconds_count), size(y,1)));
        f_idx = min(floor(Fs*(seconds_count + segment_size)), size(y,1));
        audiowrite(audio_filename, y(i_idx:f_idx, :), Fs);
        
        % Emotion scores
        while (emotion_scores(count,1) < start_end_time(1) && emotion_scores(count,1) <= start_end_time(2))
            count = count + 1;
        end    
        
        % Valence between -1 and 1. For us it's binary (0 for neg and 1 for pos)
        valence = emotion_scores(count,2);
        if (valence >= 0)
            em = 1;
        else
            em = 0;    
        end
        
        new_emotion_scores = [splice_count, em]
        emotion_scores_matrix = [emotion_scores_matrix; new_emotion_scores];
        
        % Arousal also between -1 and 1
        arousal = emotion_scores(count,3);
        if (valence >= 0)
            if (arousal >= 0)  % +H
                em = 1;
            else  % +l
                em = 2;
            end
        else
            if (arousal >= 0)  % -H
                em = 3;
            else  % -l
                em = 4;
            end
        end
        new_emotion_scores_va = [splice_count, em];
        emotion_scores_matrix_va = [emotion_scores_matrix_va; new_emotion_scores_va];
        
        new_emotion_scores_va_raw = [splice_count, emotion_scores(count,2), emotion_scores(count,3)];
        emotion_scores_matrix_va_raw = [emotion_scores_matrix_va_raw; new_emotion_scores_va_raw];
        
        splice_count = splice_count + 1;
        seconds_count = seconds_count + segment_size;
    end
    
    % Write emotion scores in csv file
    fid = fopen(strcat(path_emotion, 'intended_1.csv'),'r');
    csvwrite(strcat(path_emotion, 'intended_1.csv'), emotion_scores_matrix);
    
    % Valence and arousal
    fid = fopen(strcat(path_emotion, 'intended_1_va.csv'),'r');
    csvwrite(strcat(path_emotion, 'intended_1_va.csv'), emotion_scores_matrix_va);
    
    % Valence and arousal real values
    fid = fopen(strcat(path_emotion, 'intended_1_va_raw.csv'),'r');
    csvwrite(strcat(path_emotion, 'intended_1_va_raw.csv'), emotion_scores_matrix_va_raw);
    
end

%% Emotion
%The files are names <subject>_<iteration>_<movie>
%The file format is <time> <valence> <arousal>
