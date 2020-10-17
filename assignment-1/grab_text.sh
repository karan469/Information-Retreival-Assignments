# mkdir ../text;
# mkdir ../text/TaggedTrainingAP;
for file in ./assignment1/TaggedTrainingAP/*; do sed -n "/<TEXT>/,/<\/TEXT>/p" ${file} > ./text/${file}_text ; done
# for file in ./TaggedTrainingAP/*; do echo $file; done
