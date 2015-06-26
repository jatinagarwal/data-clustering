/* SimpleApp.scala */
import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf
import scala.util.matching.Regex

object LsaApp {
  def main(args: Array[String]) {
  	val keywords = List("abstract", "continue", "for", "new", "switch", "assert", "default", "goto", "package", "synchronized",
  		"boolean", "do", "if", "private", "this", "break", "double", "implements", "protected", "throw", "byte", "else",
  		"import", "public", "throws", "case", "enum", "instanceof", "return", "transient", "catch", "extends", "int",
  		"short", "try", "char", "final", "interface", "static", "void", "class", "finally", "long", "strictfp", "volatile",
  		"const", "float", "native", "super", "while", "true", "false", "null")

    val dataFiles = "sampleJava" // Should be some file on your system
    val conf = new SparkConf().setAppName("Lsa Application")
    val sc = new SparkContext(conf)
    val codeData = sc.wholeTextFiles(dataFiles).cache()
    codeData.persist()
    val codeDataWithOutComments = codeData.mapValues{inp => 
    	val regex = """(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*)""".r
    	val specialChar = """[^a-zA-Z\n\s\#]""".r
    	val commentsRemoved = regex.replaceAllIn(inp,"")
    	specialChar.replaceAllIn(commentsRemoved, " ")
    }	
    val words = codeDataWithOutComments.mapValues{inp =>
    	inp.split("//s+")
	}
    // val count : Int = codeData.collect().count()
    // val numAs = logData.filter(line => line.contains("a")).count()
    // val numBs = logData.filter(line => line.contains("b")).count()
    // println("Lines with a: %s, Lines with b: %s".format(numAs, numBs))
    // println("count of RDD: "+count)
    codeData.take(2).foreach(println)
    codeDataWithOutComments.take(2).foreach(println)
    words.first()
  }

  // def removeComments(inp: String): 
}