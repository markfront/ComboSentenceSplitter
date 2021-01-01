package com.markfront.corenlp.restapi;

import edu.stanford.nlp.pipeline.CoreDocument;
import edu.stanford.nlp.pipeline.CoreSentence;
import edu.stanford.nlp.pipeline.StanfordCoreNLP;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

@RestController
public class ServiceController {

    private StanfordCoreNLP pipeline;
    private Logger logger = LoggerFactory.getLogger(ServiceController.class);

    public ServiceController() {
        try {
            // set up pipeline properties
            Properties props = new Properties();
            // set the list of annotators to run
            //props.setProperty("annotators", "tokenize,ssplit,pos,lemma,ner,parse,depparse,coref,kbp,quote");
            props.setProperty("annotators", "tokenize,ssplit");
            // build pipeline
            this.pipeline = new StanfordCoreNLP(props);
            logger.info("StanfordCoreNLP pipeline created");
        } catch (Exception ex) {
            logger.error(ex.getMessage());
        }
    }

    @PostMapping("/sentsplit")
    public String[] SentSplit(
            @RequestBody String text
    ) {
        String trunc_text;
        if (text.length() > 50) {
            trunc_text = text.substring(0, 25) + " ... " + text.substring(text.length()-20);
        } else {
            trunc_text = text;
        }
        logger.info("text=" + trunc_text);
        logger.info("text.length()=" + text.length());

        // create a document object
        CoreDocument document = new CoreDocument(text);
        // annnotate the document
        this.pipeline.annotate(document);

        List<String> sentences = new ArrayList<>();
        for (CoreSentence sent : document.sentences()) {
            sentences.add(sent.text());
        }
        logger.info("sentences.length=" + sentences.size());
        return sentences.toArray(new String[0]);
    }
}
