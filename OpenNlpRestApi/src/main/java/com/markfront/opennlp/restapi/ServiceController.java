package com.markfront.opennlp.restapi;

import opennlp.tools.sentdetect.SentenceDetectorME;
import opennlp.tools.sentdetect.SentenceModel;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

import java.io.InputStream;


@RestController
public class ServiceController {
    private SentenceModel sentence_model;
    private SentenceDetectorME sentence_detector;

    Logger logger = LoggerFactory.getLogger(ServiceController.class);

    public ServiceController() {
        try {
            ClassLoader classloader = Thread.currentThread().getContextClassLoader();
            String model_file = "en-sent.bin";
            InputStream model_stream = classloader.getResourceAsStream(model_file);
            this.sentence_model = new SentenceModel(model_stream);
            this.sentence_detector = new SentenceDetectorME(this.sentence_model);
            logger.info("sentence_detector initialized using model: " + model_file);
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

        String sentences[] = this.sentence_detector.sentDetect( text);
        logger.info("sentences.length=" + sentences.length);
        return sentences;
    }
}
