import time


class StreamTimer:
    file_path = "None"
    start_time = 0
    timer_active = False
    direction = 0  # 0 is up, 1 is down
    timer_time = 0
    prev_millis = 0
    custom_time = False
    writing_to_file = False

    def milli_to_string(self, millis):
        millis = int(millis)
        negative = False
        if millis < 0:
            millis = abs(millis)
            negative = True
        seconds = (millis / 1000) % 60
        seconds = int(seconds)
        if seconds < 10:
            seconds = "0" + str(seconds)
        minutes = (millis / (1000 * 60)) % 60
        minutes = int(minutes)
        if minutes < 10:
            minutes = "0" + str(minutes)

        hours = (millis / (1000 * 60 * 60)) % 24
        hours = int(hours)
        if hours < 10:
            hours = "0" + str(hours)

        millis_s = millis % 1000
        if millis % 1000 < 10:
            millis_s = "0" + str(millis % 1000)

        millis_s = str(millis_s)
        seconds = str(seconds)
        minutes = str(minutes)
        hours = str(hours)
        if not negative:
            return "%s:%s:%s:%s" % (hours, minutes, seconds, millis_s)
        else:
            return "-%s:%s:%s:%s" % (hours, minutes, seconds, millis_s)

    def get_current_time_as_string(self):
        return self.milli_to_string(self.timer_time)

    def get_current_millis(self):
        return int(time.time() * 1000)

    def set_start_time(self):
        self.start_time = 0

    def extract_time(self, the_time):
        h, m, s, ms = [int(i) for i in the_time.split(':')]
        return int(3600 * h + 60 * m + s*1000 + ms)

    def write_to_file(self, fpath, string):
        with open(fpath, "w") as fp:
            fp.write(string)

    def reset_timer(self):
        start_time = int(0)
        self.timer_time = 0
        if self.custom_time is False:
            self.start_time = self.get_current_millis()
            self.prev_millis = self.start_time


    def pause_timer(self):
        self.deactivate_timer()

    def is_active(self):
        return self.timer_active

    def flip_direction(self):
        if self.direction is 1:
            self.direction = 0
        elif self.direction is 0:
            self.direction = 1

    def start_timer(self):
        self.activate_timer()
        if self.custom_time is False:
            self.start_time = self.get_current_millis()
            self.prev_millis = self.start_time
        else:
            self.prev_millis = self.get_current_millis()


    def activate_timer(self):
        self.timer_active = True

    def deactivate_timer(self):
        self.timer_active = False

    def set_file(self, file):
        self.file_path = file
        start_time_raw = self.get_time_from_file(self.file_path)
        if start_time_raw is not None and start_time_raw is not '' and start_time_raw is not 0:
            try:
                start_time = int(self.extract_time(start_time_raw))
                self.timer_time = start_time
                self.custom_time = True

            except Exception as e:
                print(e)
                self.reset_timer()

    def get_time_from_file(self, fp):
        try:
            with open(fp) as f:
                start_time_raw = f.readline()
            return start_time_raw
        except Exception:
            self.reset_timer()

    def set_writing_to_file(self,v):
        writing_to_file = v

    def tick(self):
        # The main loop
        curr_millis = self.get_current_millis()
        delta = int(curr_millis - self.prev_millis)
        if self.direction is 0:
            self.timer_time += delta
        elif self.direction is 1:
            self.timer_time -= delta
        disp_time = self.milli_to_string(self.timer_time)
        # print(disp_time)
        self.write_to_file(self.file_path, disp_time)
        # print("123123")
        self.prev_millis = curr_millis
