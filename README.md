# efimeriesSMS

Είναι μια υπηρεσία αποστολής sms μηνυμάτων διαβάζοντας δεδομένα απο xls αρχείο. 

Για την εφαρμογή υπάρχουν 3 φάκελοι απο όπου διαβάζει τα βασικά αρχεία. 
Στον φάκελο xml υπάρχει το αρχείο xml όπου δηλώνεται το format του xls αρχείου. 
Δηλώνεται δηλαδή ο τρόπος που είναι οργανωμένη η πληροφορία του excell αρχείου. Μέσα σε αυτό το αρχείο δηλώνεται και το όνομα του xls.
Στον φάκελο stoixeia υπάρχει αρχείο όπου αποθηκεύεται τα στοιχεία των αποδεκτών των sms μηνυμάτων. Επώνυμο, Όνομα και βέβαια κινητό τηλέφωνο. 
Στον φάκελο efimeries υπάρχει το αρχείο όπου αποθηκεύεται η πληροφορία που στέλνουμε σε μήνυμα και ακολουθεί ένα συγκεκριμένο τρόπο οργάνωσης. 
Η εφαρμογή όταν ξεκινά διαβάζει τα αρχεία των  φακέλων αυτών και στέλνει τα μηνύματα. 
Στην περίπτωση που χρειάζεται να σταλθούν μηνύματα με νέο είδος οργάνωσης, δηλαδή καινούριο xml κατ'επέκταση καινούριο xls με νέα δομή τότε δημιουργείται μια νέα διεργασία η οποία συνεχίζει την αποστολή και η οποία εκτελείται παράλληλα με την αρχική. 
Μπορεί να δημιουργηθούν τόσες νέες διεργασίες όσες είναι απαραίτητο. 
Όλες οι διεργασίες γράφουν στο ίδιο log αρχείο. 

Για την επεξεργασία των xls αρχείων χρησιμοποιήθηκε to module xlrd
και για την επεξεργασία των xml η xml.etree.ElementTree
