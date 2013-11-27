import java.io.IOException;
import java.util.HashSet;

import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.hbase.HBaseConfiguration;
import org.apache.hadoop.hbase.client.Put;
import org.apache.hadoop.hbase.client.Result;
import org.apache.hadoop.hbase.client.Scan;
import org.apache.hadoop.hbase.io.ImmutableBytesWritable;
import org.apache.hadoop.hbase.mapreduce.TableMapReduceUtil;
import org.apache.hadoop.hbase.mapreduce.TableMapper;
import org.apache.hadoop.hbase.mapreduce.TableReducer;
import org.apache.hadoop.hbase.util.Bytes;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;

public class AddTweetsToTimeTable {
  
  public static final String NAME = "add_tweets_to_time_table_in_hbase";
  
  public static final String INPUT_TABLE = "tweet";
  public static final String OUTPUT_TABLE = "time";
  public static final byte[] TIME = "time".getBytes();
  public static final byte[] TWEET = "tweet".getBytes();
  public static final byte[] TID = "tid".getBytes();

  public static class HbaseTableMapper extends TableMapper<Text, Text> {
    
    private Text time = new Text();
    private Text tweet_id = new Text();
    
    public void map(ImmutableBytesWritable row, Result columns, Context context) throws IOException, InterruptedException {
      String created_at = new String(columns.getValue(TIME, TIME));  // get value in column "user:uid"
      String tid = new String(row.get());
      time.set(created_at);
      tweet_id.set(tid);
      context.write(time, tweet_id);
    }
  }
  
  public static class HbaseTableReducer extends TableReducer<Text, Text, ImmutableBytesWritable> {
    
    public void reduce(Text key, Iterable<Text> values, Context context) throws IOException, InterruptedException {
      
      HashSet<String> tweet_set = new HashSet<String>();  // use a hashset to remove duplicates
      for (Text value : values) {
        String tid = value.toString();
        tweet_set.add(tid);
      }
      
      String tweets = "";
      for (String tweet : tweet_set) {
        tweets += tweet + "\n";
      }
      
      Put put = new Put(Bytes.toBytes(key.toString()));   // use user id as row key
      put.add(TWEET, TID, Bytes.toBytes(tweets));      // Column Family: re, Column: re_uids, Value: re_users
      context.write(null, put);
    }
  }
  
  public static void main(String[] args) throws Exception {
    Configuration conf = HBaseConfiguration.create();
    Job job = new Job(conf, NAME);
    job.setJarByClass(AddTweetsToTimeTable.class);
    
    Scan scan = new Scan();
    scan.setCaching(500);        // 1 is the default in Scan, which will be bad for MapReduce jobs
    scan.setCacheBlocks(false);  // don't set to true for MR jobs
    
    TableMapReduceUtil.initTableMapperJob(INPUT_TABLE, scan, HbaseTableMapper.class, Text.class, Text.class, job);
    TableMapReduceUtil.initTableReducerJob(OUTPUT_TABLE, HbaseTableReducer.class, job);

    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
