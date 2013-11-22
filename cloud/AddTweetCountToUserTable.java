import java.io.IOException;

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
import org.apache.hadoop.io.IntWritable;
import org.apache.hadoop.io.Text;
import org.apache.hadoop.mapreduce.Job;

public class AddTweetCountToUserTable {
  
  public static final String NAME = "add_tweet_count_to_user_table_in_hbase";
  
  public static final String INPUT_TABLE = "tweet";
  public static final String OUTPUT_TABLE = "user";
  public static final byte[] USER = "user".getBytes();
  public static final byte[] UID = "uid".getBytes();
  public static final byte[] COUNT = "count".getBytes();

  public static class HbaseTableMapper extends TableMapper<Text, IntWritable> {
    
    private final static IntWritable one = new IntWritable(1);
    private Text user_id = new Text();
    
    public void map(ImmutableBytesWritable row, Result columns, Context context) throws IOException, InterruptedException {
      String uid = new String(columns.getValue(USER, UID));  // get value in column "user:uid"
      user_id.set(uid);
      context.write(user_id, one);
    }
  }
  
  public static class HbaseTableReducer extends TableReducer<Text, IntWritable, ImmutableBytesWritable> {
    
    public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
      
      int count = 0;
      for (IntWritable value : values) {
        count += value.get();
      }
      
      Put put = new Put(Bytes.toBytes(key.toString()));   // use user id as row key
      put.add(COUNT, COUNT, Bytes.toBytes(count));   // Column Family: count, Column: count, Value: count
      context.write(null, put);
    }
  }
  
  public static void main(String[] args) throws Exception {
    Configuration conf = HBaseConfiguration.create();
    Job job = new Job(conf, NAME);
    job.setJarByClass(AddTweetCountToUserTable.class);
    
    Scan scan = new Scan();
    scan.setCaching(500);        // 1 is the default in Scan, which will be bad for MapReduce jobs
    scan.setCacheBlocks(false);  // don't set to true for MR jobs
    
    TableMapReduceUtil.initTableMapperJob(INPUT_TABLE, scan, HbaseTableMapper.class, Text.class, IntWritable.class, job);
    TableMapReduceUtil.initTableReducerJob(OUTPUT_TABLE, HbaseTableReducer.class, job);
    
//    job.setMapperClass(HbaseTableMapper.class);
//    job.setReducerClass(HbaseTableReducer.class);
//    job.setOutputFormatClass(TableOutputFormat.class);
//    job.getConfiguration().set(TableOutputFormat.OUTPUT_TABLE, OUTPUT_TABLE);
//    job.setOutputKeyClass(ImmutableBytesWritable.class);
//    job.setOutputValueClass(Writable.class);

    System.exit(job.waitForCompletion(true) ? 0 : 1);
  }
}
