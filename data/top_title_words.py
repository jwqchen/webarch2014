from mrjob.job import MRJob
from combine_user_visits import csv_readline


class topTitleWords(MRJob):


    def mapper1_extract_words(self, _, line):

        cell = csv_readline(line)
        if cell[0] == 'A':
            for word in cell[3].split():
                yield [word.lower(), 1]

    def reducer1_count_appearances(self, word, appearance_counts):
        """Sumarizes the visit counts by adding them together.  If total visits
        is more than 20, yield the results"""
        total = sum(appearance_counts)
        yield [word, total]

    def mapper2_aggregate_max(self, word, appearance_count):
        """Group reviews/counts together by the MAX statistic."""
        ###
        # By yielding using the same keyword, all records will appear in
        # the same reducer:
        yield ["MAX", [appearance_count, word]]
        ##/

    def reducer2_select_max(self, stat, count_words):
        """Given a list of pairs: [count, review_id], select on the pair with
        the maximum count, and output the result."""
        ###
        # find the review with the highest count, yield the review_id and
        # the count. HINT: the max() function will compare pairs by the first
        # number
        highest_counts = sorted(count_words, reverse=True) [0:10]
        print "The 10 most common title words:\n"
        for i in range (0, 10):
            print highest_counts[i][1], ":", highest_counts[i][0], "times"


    def steps(self):
        return [self.mr(self.mapper1_extract_words, self.reducer1_count_appearances),
                self.mr(self.mapper2_aggregate_max, self.reducer2_select_max)]

if __name__ == '__main__':
    topTitleWords.run()